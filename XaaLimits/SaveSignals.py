from coffea.nanoevents import NanoEventsFactory, NanoAODSchema
from coffea import processor
import uproot as up
import awkward as ak
import numpy as np
import json
import matplotlib.pyplot as plt
from Pairing import PairDeltaR, PairMA, unique_pairing_perms
from plotting import ConvertToROOT
NanoAODSchema.warn_missing_crossrefs=False

#define files here (JSON format) 
fileset = {
    "name": {
        "files": {
            "path/to/file.root" : "Events"
        },
        
        "metadata": {
            "is_mc": True
        }
    }
}

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
        #trigger = events.HLT.Diphoton30_22_R9Id_OR_IsoCaloId_AND_HE_R9Id_Mass90 # Run 2 2016-2017 trigger
        trigger = events.HLT.TriplePhoton_35_35_5_CaloIdLV2_R9IdVL # Run 2 2017-2018 trigger
        all_photons = events.Photon[(ak.num(events.Photon) >= 4) & trigger] #Grab events

        # Check if photon is in barrel or endcap #
        isEB = abs(all_photons.eta) < 1.48
        isEE = abs(all_photons.eta) >= 1.48

        # Define MVA_cut for each photon #
        MVA_cut1 = ((isEB & (all_photons.mvaID[:,0] >= 0.27)) |      # barrel threshold
                (isEE & (all_photons.mvaID[:,0] >= 0.14)))       # endcap threshold

        MVA_cut2 = ((isEB & (all_photons.mvaID[:,1] >= 0.27)) |
                (isEE & (all_photons.mvaID[:,1] >= 0.14)))
        
        MVA_cut3 = ((isEB & (all_photons.mvaID[:,2] >= 0.27)) |
                (isEE & (all_photons.mvaID[:,2] >= 0.14)))

        MVA_cut4 = ((isEB & (all_photons.mvaID[:,3] >= 0.27)) |
                (isEE & (all_photons.mvaID[:,3] >= 0.14)))
        
        MVA_cut =  (MVA_cut1) & (MVA_cut2) & (MVA_cut3)
        photons_wMVA = all_photons[MVA_cut] # applies MVA selection

        # Filter any events that have too few photons after MVA cut #
        photons_presel = photons_wMVA[ak.num(photons_wMVA) >= 4]

        # Now take the 4 leading photons from every event #
        photons = photons_presel[:,:4]

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
        alpha = PhiM/X.mass
        DR1 = photons[:,0].deltaR(photons[:,1])
        DR2 = photons[:,2].deltaR(photons[:,3])
        mass_asym = abs(Phi0.mass - Phi1.mass)/(Phi0.mass + Phi1.mass)
        DeltaEta = abs(Phi0.eta - Phi1.eta)

        # Region A Cuts #
        X = X[(DR1 < 1.0) & (mass_asym < 0.1)]
        
        # Region B filter #
        DRcuts = (DR1 < 2.75) & (DR2 < 2.75)
        #X = X[(DR1 >= 1.0) & DRcuts & (mass_asym < 0.1) & (DeltaEta < 1.9)] #full cut
        #X = X[(DR1 >= 1.0)]# & (mass_asym < 0.1)] # relaxed cut

        Xm = X.mass

        return {
            dataset: {
                "entries": len(events),
                "mass" : Xm.tolist(),
                "yield" : len(Xm)
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

# Signals #
X200 = np.array(out["X200"]["mass"])
X300 = np.array(out["X300"]["mass"])
X500 = np.array(out["X500"]["mass"])
X750 = np.array(out["X750"]["mass"])
X1000 = np.array(out["X1000"]["mass"])
X1500 = np.array(out["X1500"]["mass"])
X2000 = np.array(out["X2000"]["mass"])
X3000 = np.array(out["X3000"]["mass"])

# Create event weights for if we need to reweight later #
weights500 = np.ones_like(X500)
weights750 = np.ones_like(X750)
weights1000 = np.ones_like(X1000)
weights1500 = np.ones_like(X1500)
weights2000 = np.ones_like(X2000)
weights3000 = np.ones_like(X3000)

# Make ROOT plots
with up.recreate("shapes.root") as fout:
    # Create a TTree named "events" with one branch "mass"
    fout["signal_m500"] = {"mass": X500,
                           "weights": weights500}
    fout["signal_m750"] = {"mass": X750,
                           "weights": weights750}
    fout["signal_m1000"] = {"mass": X1000,
                           "weights": weights1000}
    fout["signal_m1500"] = {"mass": X1500,
                           "weights": weights1500}
    fout["signal_m2000"] = {"mass": X2000,
                           "weights": weights2000}
    fout["signal_m3000"] = {"mass": X3000,
                           "weights": weights3000}

plt.close()

# Dump a file with reconstruction efficiencies for limit setting #
mrange = ["X500","X750","X1000","X1500","X2000","X3000"]
yields = [out[m]["yield"] for m in mrange]
totals = [out[m]["entries"] for m in mrange]
efficiencies = [round(a/b,2) for a,b in zip(yields,totals)]
out2json = {key: value for key, value in zip(mrange, efficiencies)}
with open("alphaval_eff.json", "w") as json_file:
        json.dump(out2json, json_file, indent=4)'''
