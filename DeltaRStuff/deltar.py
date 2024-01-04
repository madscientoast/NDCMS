from ROOT import TH1D, TFile, TLorentzVector, TCanvas
import time

def FindAndSetMax(h): 
	maximum = 0.0
	h.SetStats(0)
	t = h.GetMaximum()
	if t > maximum:
		maximum = t
	h.GetYaxis().SetRangeUser(0,maximum*1.35)#should be 1.35 (below as well)
	h.SetLineWidth(2)
	return maximum*1.35


c = TCanvas()
h = TH1D("h1", "dR [X300A15]", 2000, 0.0, 100.0)
f = TFile.Open("X3000A750/3A3C76AE-9E9D-5545-8A4C-B4E443FE2F36.root")
events = f.Events

start = time.time()
for e in range(0,events.GetEntries()):
    events.GetEntry(e) 
    pt = events.Photon_pt
    eta = events.Photon_eta
    phi = events.Photon_phi 
    m = events.Photon_mass
    for i in range(0,len(pt)):
        photon0 = TLorentzVector()
        photon0.SetPtEtaPhiM(pt[i],eta[i],phi[i],m[i])
        for j in range(0,len(pt)):
            if i >= j:
                continue
            photon1 = TLorentzVector()
            photon1.SetPtEtaPhiM(pt[j],eta[j],phi[j],m[j])
            dR = photon1.DeltaR(photon0)
            h.Fill(dR)

print("Time Elapsed: ", time.time()-start) 

x = h.GetXaxis()
FindAndSetMax(h)
x.SetRangeUser(0, 10)
h.Draw()
c.SaveAs("X300A15/test.pdf")