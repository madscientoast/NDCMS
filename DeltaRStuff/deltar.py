from ROOT import TH1D, TFile, TLorentzVector, TCanvas

c = TCanvas()
h = TH1D("h1", "dR [X300A15]", 1000, 0.0, 100.0)
f = TFile.Open("X300A15/8FC216FE-6399-6845-8572-36A5078139F1.root")
events = f.Events

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

x = h.GetXaxis()

h.SetStats(0)
h.Rebin(1)
x.SetRange(0, 100)
h.Draw()
c.SaveAs("X300A15/test2.pdf")