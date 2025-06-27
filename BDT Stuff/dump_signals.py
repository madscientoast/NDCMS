from ROOT import *
from itertools import combinations
from math import floor,sqrt
from fmt import *
from kinematics import *
from pairing import *

#Open Files and Create Histograms
base = "06-27-2025/"
files = ["X300A15/result.root", "X300A30/result.root", "X300A75/result.root"]
out_files = [base+"signal15.txt", base+"signal30.txt", base+"signal75.txt"] 

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

for i in range(len(files)):
    f = TFile.Open(files[i])
    events = f.Events
    with open(out_files[i],'a') as file:
        for e in range(0,events.GetEntries()):
            events.GetEntry(e)
            nPhoton = events.nPhoton
            trigger = events.HLT_TriplePhoton_35_35_5_CaloIdLV2_R9IdVL
            if nPhoton >= 4 and trigger == 1:
                pt = events.Photon_pt
                eta = events.Photon_eta
                phi = events.Photon_phi 
                m = events.Photon_mass
                mva = events.Photon_mvaID
                veto = events.Photon_electronVeto
                iso = events.Photon_pfRelIso03_all
                vec = [[pt[i],eta[i],phi[i],0] for i in range(4)]
                vec = MVAcut(mva,veto,vec) #Apply MVA cut
                if len(vec) < 4:
                    continue
                pair = MakePairs(vec)
                index = ChoosePair("dR",pair)
                photon0,photon1,photon2,photon3 = CreatePhotons(pair,index)
                phi0 = photon0+photon1
                phi1 = photon2+photon3
                X = phi0+phi1
                Phi_mass = (phi0.M()+phi1.M())/2
                Xm = X.M()
                DeltaR1 = photon0.DeltaR(photon1)
                DeltaR2 = photon2.DeltaR(photon3)
                DeltaEta = abs(phi0.Eta() - phi1.Eta())
                MassAsym = abs(phi0.M() - phi1.M()) / (phi0.M() + phi1.M())
                file.write(f"{Xm:.6f}\t{Phi_mass:.6f}\t{DeltaR1:.6f}\t{DeltaR2:.6f}\t{DeltaEta:.6f}\t{MassAsym:.6f}\n")
        
    


