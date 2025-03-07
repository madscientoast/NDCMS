# Import the Stuff #
from ROOT import *
from itertools import combinations
from math import floor,sqrt
from fmt import *
from kinematics import *
from pairing import *

#Open Files and Create Histograms
#f = TFile.Open("X300A15/result.root") #MC input
#f = TFile.Open("X300A30/result.root") #MC input
#f = TFile.Open("X300A75/result.root") #MC input
f = TFile.Open("~/DataFiles/merged_output.root") # 1.1 fb Data input
events = f.Events 

# MVAID cut #
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

# Loop for writing info to file, just change file filename as needed #
with open("03-03-2025/bkg.txt",'a') as file:
    for e in range(0,events.GetEntries()): 
        events.GetEntry(e)
        nPhoton = events.nPhoton
        trigger = events.HLT_TriplePhoton_35_35_5_CaloIdLV2_R9IdVL

        # Ensure we have at least 4 photons that pass the trigger
        if nPhoton >= 4 and trigger == 1:
            # Load event level variables #
            pt = events.Photon_pt
            eta = events.Photon_eta
            phi = events.Photon_phi 
            m = events.Photon_mass
            mva = events.Photon_mvaID
            veto = events.Photon_electronVeto
            # Construct 4-vectors of (p_t, eta, phi, m)
            vec = [[pt[i],eta[i],phi[i],0] for i in range(4)]
            vec = MVAcut(mva,veto,vec) #Apply MVA cut
            # Ensure we have events with at least 4 photons that pass the trigger and MVAID 
            if len(vec) < 4:
                continue
            # Performing Pairing Algorithm
            pair = MakePairs(vec)
            index = ChoosePair("dR",pair)

            # Make photons as TLorentzVectors now
            photon0,photon1,photon2,photon3 = CreatePhotons(pair,index)

            #Construct Phi Particles (Parents of Diphoton Pairs)
            phi0 = photon0+photon1
            phi1 = photon2+photon3

            #Construct X particle(s) (4-mass)
            X = phi0+phi1

            # Evaluate all results we want#
            Xm = X.M()
            PhiMasses = [phi0.M(),phi1.M()]
            avgPhi = (PhiMasses[0]+PhiMasses[1])/2
            ma = abs(PhiMasses[0]-PhiMasses[1])/(PhiMasses[0]+PhiMasses[1])
            dR1 = photon1.DeltaR(photon0)
            dR2 = photon3.DeltaR(photon2)
            dEta = abs(phi0.Eta() - phi1.Eta())

            # Dump to Tab-separated Text file #
            # Formatting is: m_phi  m_x  m_asym  dEta  dR1  dR2 #
            avgPhi_toFile = f'{avgPhi}\t'
            XmToFile = f'{Xm}\t'
            ma_toFile = f'{ma}\t'
            dEta_toFile = f'{dEta}\t'
            dR1_toFile = f'{dR1}\t'
            dR2_toFile = f'{dR2}\n'
            file.write(avgPhi_toFile)
            file.write(XmToFile)
            file.write(ma_toFile)
            file.write(dEta_toFile)
            file.write(dR1_toFile)
            file.write(dR2_toFile)
        
    


