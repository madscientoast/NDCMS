Workflow:

1. data_dump.py 
    I use this to reconstruct all relevant information from each event and dump into files for MC and Data

2. MakeTree.py
    After dumping info to text files for MC and Data, load these up into TTrees with masses and kinematic variables
    Basically preps signal and data for making BDT

3. MVA_BDT.py
    Input the data and signal ROOT files, outputs BDT ROOT file and weights. 

4. FilterData.py
    Apply BDT weights to Data and output (binned or unbinned version)

5. BinSignals.py (Optional)
    Bin Signal 4-mass 

From here we can just take outputs and use to make workspaces for COMBINE
