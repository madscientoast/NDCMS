from ROOT import *
from itertools import combinations
from math import floor,sqrt
from fmt import *
from kinematics import *
from pairing import *

#Open Files and Create Histograms
f = TFile.Open("X300A75/result.root")
events = f.Events 
canv = TCanvas()
h = TH1D("h1", "Average Mass [MC]", 100, 0.0, 100.0)

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

for e in range(0,events.GetEntries()): 
    events.GetEntry(e)
    nPhoton = events.nPhoton
    trigger = events.HLT_TriplePhoton_35_35_5_CaloIdLV2_R9IdVL
    if nPhoton == 4 and trigger == 1:
        pt = events.Photon_pt
        eta = events.Photon_eta
        phi = events.Photon_phi 
        m = events.Photon_mass
        mva = events.Photon_mvaID
        veto = events.Photon_electronVeto
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
        Xm = X.M()
        PhiMasses = [phi0.M(),phi1.M()]
        PhiEtas = [phi0.Eta(),phi1.Eta()]
        Etta = abs(PhiEtas[0]-PhiEtas[1])
        avgPhi = (PhiMasses[0]+PhiMasses[1])/2
        ma = abs(PhiMasses[0]-PhiMasses[1])/(PhiMasses[0]+PhiMasses[1])
        dR1 = photon1.DeltaR(photon0)
        dR2 = photon3.DeltaR(photon2)
        h.Fill(avgPhi)
        #if ma < 0.1 and Etta < 1.1 and dR1 < 2.0 and dR2 < 2.0:
        '''if dR1 < 2.0 and dR2 < 2.0 and ma < 0.1 and Etta < 1.1:
            h.Fill(avgPhi)
        else:
            continue'''
    
#Drawing Time
x = h.GetXaxis()
y = h.GetYaxis()
x.SetTitle("Average Mass [GeV]")
y.SetTitle("Events")
FindAndSetMax(h)
h.Draw("E")
print(h.GetRMS())
#canv.SetLogx()
canv.SaveAs("GetSTDEV-75.root")
