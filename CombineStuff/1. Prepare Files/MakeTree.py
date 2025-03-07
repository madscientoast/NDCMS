from ROOT import TFile, TTree
from array import array

# Initialize lists to store data from the text file
m_avg = []
m_Xm = []
m_asym = []
deltaEta = []
dR1 = []
dR2 = []

# Read the tab-separated file
with open("01-27-2025/bkg.txt", 'r') as file:
    # Loop through each line in the file
    for line in file:
        # Split by tabs and read as floats
        values = line.strip().split("\t")
        m_avg.append(float(values[0]))
        m_Xm.append(float(values[1]))
        m_asym.append(float(values[2]))
        deltaEta.append(float(values[3]))
        dR1.append(float(values[4]))
        dR2.append(float(values[5]))

# Initialize a ROOT file to save the TTree
output_file = TFile("01-27-2025/bkg.root", "RECREATE")

# Create a TTree with the expected variables
tree = TTree("Events", "Contains m_avg, m_Xm, m_asym, deltaEta, dR1, dR2")

# Define arrays for each branch (needed for ROOT to write data)
avg = array('f', [0])
Xm = array('f', [0])
asym = array('f', [0])
dEta = array('f', [0])
dr1 = array('f', [0])
dr2 = array('f', [0])

# Create branches in the TTree
tree.Branch("m_avg", avg, "m_avg/F")
tree.Branch("m_Xm", Xm, "m_Xm/F")
tree.Branch("m_asym", asym, "m_asym/F")
tree.Branch("deltaEta", dEta, "deltaEta/F")
tree.Branch("dR1", dr1, "dR1/F")
tree.Branch("dR2", dr2, "dR2/F")

# Fill the tree with data
for i in range(len(m_avg)):
    avg[0] = m_avg[i]
    Xm[0] = m_Xm[i]
    asym[0] = m_asym[i]
    dEta[0] = deltaEta[i]
    dr1[0] = dR1[i]
    dr2[0] = dR2[i]
    tree.Fill()

# Write the tree to the output file
tree.Write()
output_file.Close()

