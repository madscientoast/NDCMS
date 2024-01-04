from ROOT import TH1D, TFile, TLorentzVector, TCanvas
from itertools import combinations
from more_itertools import unique_everseen
import time

def FindAndSetMax(h): #Marc's code
	maximum = 0.0
	h.SetStats(0)
	t = h.GetMaximum()
	if t > maximum:
		maximum = t
	h.GetYaxis().SetRangeUser(0,maximum*1.35)#should be 1.35 (below as well)
	h.SetLineWidth(2)
	return maximum*1.35

canv = TCanvas()
h = TH1D("h1", "dR [X300A15]", 2000, 0.0, 100.0)
f = TFile.Open("X300A15/8FC216FE-6399-6845-8572-36A5078139F1.root")
events = f.Events

start = time.time()

for e in range(0,events.GetEntries()):
    events.GetEntry(e)
    pt = events.Photon_pt
    eta = events.Photon_eta
    phi = events.Photon_phi 
    m = events.Photon_mass
    vec = [[pt[i],eta[i],phi[i],m[i]] for i in range(len(pt))]
    comb = unique_everseen(combinations(vec,2))
    for c in comb:
        photon0 = TLorentzVector()
        photon1 = TLorentzVector()
        photon0.SetPtEtaPhiM(c[0][0],c[0][1],c[0][2],c[0][3])
        photon1.SetPtEtaPhiM(c[1][0],c[1][1],c[1][2],c[1][3])
        dR = photon1.DeltaR(photon0)
        h.Fill(dR)

print("Time Elapsed: ", time.time()-start) 

x = h.GetXaxis()
FindAndSetMax(h)
x.SetRangeUser(0, 10)
h.Draw()
canv.SaveAs("X300A15/test2.pdf")