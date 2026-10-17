
from coffea.nanoevents import NanoAODSchema
from coffea import processor
import uproot as up
import awkward as ak
import numpy as np
from Pairing import PairDeltaR, PairMA, unique_pairing_perms
import correctionlib
import sys
import json
NanoAODSchema.warn_missing_crossrefs=False

run_year = str(sys.argv[1])
run_era = str(sys.argv[2])
signal_region = str(sys.argv[3])
alpha = str(sys.argv[4])

# Load in files #
with open("/path/to/"+run_year+"_"+run_era+"_"+alpha+"_Dataset.json") as f:
    fileset = json.load(f)

# Load in json for MVAID/eveto SFs
if run_era == "preVFP":
    cset_mva = correctionlib.CorrectionSet.from_file("/path/to/sf/"+run_year+"/photon_preVFP.json.gz")
    cset_pu = correctionlib.CorrectionSet.from_file("/path/to/sf/"+run_year+"/puWeights_preVFP.json.gz")
else:
    cset_mva = correctionlib.CorrectionSet.from_file("/path/to/sf/"+run_year+"/photon.json.gz")
    cset_pu = correctionlib.CorrectionSet.from_file("/path/to/sf/"+run_year+"/puWeights.json.gz")

phoID = cset_mva["UL-Photon-ID-SF"]

if run_year == "2016":
    pileup = cset_pu["Collisions16_UltraLegacy_goldenJSON"]
if run_year == "2017A" or run_year == "2017B":
    pileup = cset_pu["Collisions17_UltraLegacy_goldenJSON"]
if run_year == "2018":
    pileup = cset_pu["Collisions18_UltraLegacy_goldenJSON"]

# Define What to actually do here #
class MyProcessor(processor.ProcessorABC):
    def __init__(self, mode="virtual"):
        assert mode in ["eager", "virtual", "dask"]
        self._mode = mode
    
    @property
    def accumulator(self):
        return self._accumulator

    def process(self, events):
        dataset = events.metadata['dataset']
        if run_year == "2016":
            trigger = events.HLT.Diphoton30_18_R9Id_OR_IsoCaloId_AND_HE_R9Id_Mass90 & (events.Photon[:,1].pt >= 70.0) # 2016 Trigger with required pt cut
        if run_year == "2017A":
            trigger = events.HLT.Diphoton30_22_R9Id_OR_IsoCaloId_AND_HE_R9Id_Mass90 & (events.Photon[:,1].pt >= 70.0) # 2017A Trigger with required pt cut
        else:
            trigger = events.HLT.TriplePhoton_35_35_5_CaloIdLV2_R9IdVL # Trigger for rest of Run 2

        all_photons = events.Photon[(ak.num(events.Photon) >= 4) & trigger]
        piles = events.Pileup[(ak.num(events.Photon) >= 4) & trigger]


        # Apply MVAID #
        MVA_cut = (all_photons.mvaID_WP90) & (all_photons.electronVeto)
        photons_wMVA = all_photons[MVA_cut] # apply MVA
        sr_mask = ak.num(photons_wMVA) >= 4

        # Filter any events that have too few photons after MVA cut #
        piles_presel = piles[sr_mask]
        photons_presel = photons_wMVA[sr_mask]

        # Now take the 4 leading photons from every event #
        photons = photons_presel[:,:4]

        # Process some scale factors #
        pu_nom = pileup.evaluate(piles_presel.nTrueInt,"nominal")

        if run_year == "2016" and run_era == "preVFP":
            phoIDyear = "2016preVFP"
        if run_year == "2016" and run_era == "postVFP":
            phoIDyear = "2016postVFP"
        else:
            phoIDyear = run_year

        pt_eval = ak.where(photons.pt >= 500, 499.0, ak.where(photons.pt < 20, 20.0, photons.pt))
        phoSF_i = phoID.evaluate(phoIDyear, "sf", "wp90", photons.eta, pt_eval)
        phoSF = ak.where(photons.pt < 20,1.0,phoSF_i)

        initial_event_weight = phoSF[:,0]*phoSF[:,1]*phoSF[:,2]*phoSF[:,3]*pu_nom

        # Now to pick best combo
        combos = np.array(unique_pairing_perms(4))
        dR_idx, dR_min = PairDeltaR(photons)
        DR_perm_idx = ak.Array(combos)[dR_idx]
        PairDRFlag = (dR_min < 1.0)
        PairMAFlag = (dR_min >= 1.0)

        # Get Region A photons #
        DRphotons = photons[DR_perm_idx]
        DRphotons = DRphotons[PairDRFlag]

        # Get Region B photons #
        MA_photons_unpaired = photons[PairMAFlag]
        MA_idx = PairMA(MA_photons_unpaired)
        MA_perm_idx = ak.Array(combos)[MA_idx]
        MAphotons = MA_photons_unpaired[MA_perm_idx]

        combined_Photons = ak.concatenate([DRphotons,MAphotons])

        photons = ak.zip({
            "pt": combined_Photons.pt,
            "eta": combined_Photons.eta,
            "phi": combined_Photons.phi,
            "mass": ak.zeros_like(combined_Photons.pt)  # same shape as pt
        }, with_name="Momentum4D")

        # Now put together parent particles
        Phi0 = photons[:,0] + photons[:,1]
        Phi1 = photons[:,2] + photons[:,3]
        X = Phi0 + Phi1
        
        PhiM = (Phi0.mass + Phi1.mass)/2
        DR1 = photons[:,0].deltaR(photons[:,1])
        DR2 = photons[:,2].deltaR(photons[:,3])
        mass_asym = abs(Phi0.mass - Phi1.mass)/(Phi0.mass + Phi1.mass)
        DeltaEta = abs(Phi0.eta - Phi1.eta)

        # Evaluate RPT #
        photons_sorted = photons[ak.argsort(photons.pt, axis=1, ascending=False)]
        photons_lead3 = photons_sorted[:, :3]
        photon4 = photons_sorted[:, 3]
        pt4 = photon4.pt
        avg_pt123 = ak.mean(photons_lead3.pt, axis=1)
        RPT = pt4/avg_pt123
        RPT_sel = (RPT >= 0.14)
        
        # Region Filters #
        srA = (DR1 < 1.0) & (mass_asym < 0.1) & RPT_sel
        srB = (DR1 >= 1.0) & (mass_asym < 0.1) & (DR1 < 2.75) & (DR2 < 2.75) & RPT_sel

        if signal_region == "A":
            X = X[srA]
            event_weight = initial_event_weight[srA]
        else:
            X = X[srB]
            event_weight = initial_event_weight[srB]

        Xm = X.mass

        return {
            dataset: {
                "entries": len(events),
                "Xm" : Xm.tolist(),
                "weights" : event_weight.tolist()
            }
        }
    
    def postprocess(self, accumulator):
        merged = []
        for sublist in accumulator:
            merged.extend(sublist)
        return merged
        

# Do things here #
iterative_run = processor.Runner(
    executor = processor.FuturesExecutor(workers=4, compression=None),
    schema=NanoAODSchema,
    chunksize=1000000,
    savemetrics=True,
)

out, metrics = iterative_run(
    fileset,
    processor_instance=MyProcessor("virtual"),
)

Xs = out["Background"]["Xm"]
weights = out["Background"]["weights"]

# Make ROOT plots
with up.recreate("shapes_"+alpha+"_SR"+signal_region+"_"+run_year+"_"+run_era+".root") as fout:
    # Create a TTree named "events" with one branch "mass"
    fout["data_obs"] = {"mass": Xs,
                        "weights": weights}
