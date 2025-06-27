from ROOT import *
from itertools import combinations
from math import floor,sqrt
from fmt import *
from kinematics import *
from pairing import *
import time

t_initial = time.time()

#Open Files and Create Histograms
#f = TFile.Open("X300A30/result.root") #MC input
#f = TFile.Open("/project01/ndcms/atownse2/RSTriPhoton/data/NanoAODv9/EGamma_Run2018D-UL2018_MiniAODv2_NanoAODv9-v3_1.root") #Data File
#f = TFile.Open("~/DataFiles/EGamma_Run2018D-UL2018_MiniAODv2_NanoAODv9-v3_1.root")
#f = TFile.Open("~/DataFiles/merged_output.root")
#f = TFile.Open("/scratch365/rsnuggs/CMSSW_14_1_0_pre4/src/NanoAOD_Test.root")
#f = TFile.Open("/users/rsnuggs/CMSSW_VERSIONS/CMSSW_12_2_3/src/NPS-X300A20_1/NPS-X300A20_1_1000_NanoAOD.root")
#f = TFile.Open("~/NanoAOD_10k_1.root")
f = TFile.Open("~/CMSSW_VERSIONS/CMSSW_13_2_9/src/X1000_A150_NanoAOD_1.root")
events = f.Events 
canv = TCanvas()
#h = TH1D("h1", "\\alpha", 100, 0.0, 1.0)
#h = TH1D("h1", "4-Mass [MC, S = 30 GeV]", 1000, 0.0, 2000.0)
#h = TH1D("h1", "4-mass [Data]",100,0.0,2000.0)
#h = TH1D("h1", "Average Mass [Data]", 100, 0.0, 200.0)
#h = TH1D("h1","",100,0.0,400.0) #avg mass
#h = TH1D("h1", "",2000,0.0,2000.0)
h = TH1D("h1", "",100,0.0,500.0)
h = TH1D("h1", "",100,750.0,1250.0)

def MVAcut(id,v,lst): #90% cut at present
    result = []
    for i in range(len(lst)):
        if v[i] == 1: #Apply electron veto
            if lst[i][1] > 1.4: #Check eta to see if in endcap
                if id[i] > 0.14: #apply endcap cut
                    continue
                else:
                    result.append(lst[i])
            else: #in barrel
                if id[i] > 0.27: #apply barrel cut
                    continue
                else:
                    result.append(lst[i])
        else:
            continue
    return result

def FindInBin(h,value):
    for i in range(100):
        if h.GetBinLowEdge(i) == value or h.GetBinCenter(i) == value or h.GetBinLowEdge(i)+h.GetBinCenter(i) == value:
            return i


for e in range(events.GetEntries()): 
    events.GetEntry(e)

    # Check for the basic conditions early to exit quickly if not satisfied
    if events.nPhoton < 4:# or not events.HLT_TriplePhoton_35_35_5_CaloIdLV2_R9IdVL:
        continue

    # Access only the first four photons manually (as multi-dimensional slicing is not supported)
    pt = events.Photon_pt
    eta = events.Photon_eta
    phi = events.Photon_phi 
    mva = events.Photon_mvaID
    veto = events.Photon_electronVeto

    # Use MVAcut to filter photons based on MVA ID and veto conditions
    #vec = MVAcut(mva, veto, [[pt[i], eta[i], phi[i], 0] for i in range(4)]) 
    vec = [[pt[i], eta[i], phi[i], 0] for i in range(4)]
    
    # If MVAcut reduces the photon count to below 4, skip
    if len(vec) < 4:
        continue

    # Generate diphoton pairs and select the best pairing based on deltaR
    pair = MakePairs(vec)
    index = ChoosePair("dR", pair)

    # Create photon TLorentzVector objects
    photon0, photon1, photon2, photon3 = CreatePhotons(pair, index)

    # Compute invariant masses
    phi0 = photon0 + photon1
    phi1 = photon2 + photon3
    X = phi0 + phi1
    Xm = X.M()

    # Calculate mass asymmetry and check the condition
    ma = abs(phi0.M() - phi1.M()) / (phi0.M() + phi1.M())

    # Fill the histogram if mass asymmetry condition is met
    #if ma < 0.6:
    h.Fill(Xm)



t_final = time.time()      

#Drawing Time
x = h.GetXaxis()
y = h.GetYaxis()
#x.SetTitle("Average Mass [GeV]")
x.SetTitle("4-mass [GeV]")
y.SetTitle("Events")
FindAndSetMax(h)
#hist.SetLineColor(1)
h.Draw("E")
AddCMSLumi(canv,1.1,"Preliminary")
#canv.SetLogx()
#canv.SaveAs("06-27-2024/Attempt1/DataAverageMasswithMA+alphaCuts.root")

'''
smallsum = 0
for bin in range(25):
    smallsum += h.GetBinContent(bin)

print(smallsum)'''

'''
#bins15 = [FindInBin(h,7.0),FindInBin(h,23.0)]
#bins30 = [FindInBin(h,15.0),FindInBin(h,45.0)]
bins75 = [FindInBin(h,62.0),FindInBin(h,88.0)]
#sum15 = h.Integral(bins15[0],bins15[1])
#sum30 = h.Integral(bins30[0],bins30[1])
sum75 = h.Integral(bins75[0],bins75[1])
#tot = sum15+sum30+sum75
#print(sum15,sum30,sum75)
#print(tot)
print(sum75)
print(h.Integral(FindInBin(h,0.0),FindInBin(h,100.0)))'''

#print(h.Integral())
elapsed_time = t_final - t_initial
#canv.SaveAs("03-03-2025/4m_15GeV_PreBDT.root")
import os
# Ensure output directory exists
output_dir = "03-03-2025"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

outfile = TFile(f"X1000A150_notrigMVA.root", "RECREATE")

# Check if histogram is valid
if h is None:
    print("Error: h_extended is None before writing!")
    exit(1)

# Ensure histogram stays in memory
h.SetDirectory(0)
h.Write("data_obs")
outfile.Close()
print(f"Time elapsed: {elapsed_time:.2f} seconds")
