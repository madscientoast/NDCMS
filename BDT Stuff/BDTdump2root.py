import ROOT
from array import array

# Open the background ROOT file
background_file = ROOT.TFile("bkg.root")
background_tree = background_file.Get("Events")

# Load the trained BDT model
reader = ROOT.TMVA.Reader()

# Define variables (matching the training setup)
m_asym = array('f', [0])
deltaEta = array('f', [0])
dR1 = array('f', [0])
dR2 = array('f', [0])

reader.AddVariable("m_asym", m_asym)
reader.AddVariable("deltaEta", deltaEta)
reader.AddVariable("dR1", dR1)
reader.AddVariable("dR2", dR2)

# Load the BDT weights
reader.BookMVA("BDT", "dataset/weights/TMVAClassification_BDT.weights.xml")

# BDT cut threshold
bdt_cut = 0.185

# Create the output ROOT file and tree
output_file = ROOT.TFile("bkg_filtered.root", "RECREATE")
output_tree = ROOT.TTree("Events", "Filtered Events Tree")

# Define output branches
m_avg_out = array('f', [0])
m_Xm_out = array('f', [0])

output_tree.Branch("m_avg", m_avg_out, "m_avg/F")
output_tree.Branch("m_Xm", m_Xm_out, "m_Xm/F")

# Apply the BDT cut and fill the new tree
for event in background_tree:
    m_asym[0] = event.m_asym
    deltaEta[0] = event.deltaEta
    dR1[0] = event.dR1
    dR2[0] = event.dR2

    bdt_score = reader.EvaluateMVA("BDT")

    if bdt_score > bdt_cut:
        m_avg_out[0] = event.m_avg
        m_Xm_out[0] = event.m_Xm
        output_tree.Fill()

# Write the output tree to the file
output_file.Write()
output_file.Close()

print("Filtered background data saved to 'bkg_filtered.root' with the Events tree.")