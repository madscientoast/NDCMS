from coffea.nanoevents import NanoEventsFactory, NanoAODSchema
from coffea import processor
import uproot as up
import awkward as ak
import numpy as np
from Pairing import PairDeltaR, PairMA, unique_pairing_perms
NanoAODSchema.warn_missing_crossrefs=False

fileset = {
    "Background": {
        "files": {
            # files here #
        },
        "metadata": {
            "is_mc": False
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
        #trigger =  events.HLT.DoublePhoton85 # old trigger
        trigger = events.HLT.Diphoton30_18_R9Id_OR_IsoCaloId_AND_HE_R9Id_Mass90 # Run 2 2016-2017 trigger

        all_photons = events.Photon[(ak.num(events.Photon) >= 4) & trigger]
        all_photons = all_photons[(all_photons.pt[:,1] >= 22.0)] # Applying a pt cut on the second photon to match the trigger to the updated one in the MC #
        
      # Check if photon is in barrel or endcap #
        isEB = abs(all_photons.eta) < 1.48
        isEE = abs(all_photons.eta) >= 1.48
        
        # Define MVA_cut for each photon #
        MVA_cut1 = ((isEB & (all_photons.mvaID[:,0] >= 0.27)) |      # barrel threshold
                (isEE & (all_photons.mvaID[:,0] >= 0.14)))       # endcap threshold

        MVA_cut2 = ((isEB & (all_photons.mvaID[:,1] >= 0.27)) |      # barrel threshold
                (isEE & (all_photons.mvaID[:,1] >= 0.14)))       # endcap threshold
        
        MVA_cut3 = ((isEB & (all_photons.mvaID[:,2] >= 0.27)) |      # barrel threshold
                (isEE & (all_photons.mvaID[:,2] >= 0.14)))       # endcap threshold

        MVA_cut4 = ((isEB & (all_photons.mvaID[:,3] >= 0.27)) |      # barrel threshold
                (isEE & (all_photons.mvaID[:,3] >= 0.14)))       # endcap threshold

        MVA_cut =    (MVA_cut1)# & (MVA_cut2) & # & (MVA_cut3)
        invert_MVA = ~MVA_cut # for CR
        photons_wMVA = all_photons[MVA_cut] # apply MVA

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
                "Xm" : Xm.tolist()
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

# Load events #
num_events = out["Background"]["entries"]
print("Number of events: ", num_events)

Xs = out["Background"]["Xm"]
print("Num of events after selections: ",len(Xs))

weights = np.ones_like(Xs)

# Make ROOT plots
with up.recreate("bkgA_2016.root") as fout:
    # Create a TTree named "events" with one branch "mass"
    fout["data_obs"] = {"mass": Xs,
                        "weights": weights}
