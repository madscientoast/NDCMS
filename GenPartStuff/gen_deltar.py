from ROOT import TFile, TLorentzVector, TCanvas, TH1D

c = TCanvas()
h = TH1D("h1", "dR [X300A15]", 2000, 0.0, 100.0)
f = TFile.Open("X300A15/7F4DE753-B11F-B445-A7FE-C0E7728CE935.root")
events = f.Events

def FindAndSetMax(h): 
	maximum = 0.0
	h.SetStats(0)
	t = h.GetMaximum()
	if t > maximum:
		maximum = t
	h.GetYaxis().SetRangeUser(0,maximum*1.35)#should be 1.35 (below as well)
	h.SetLineWidth(2)
	return maximum*1.35

for e in range(events.GetEntries()):
    events.GetEntry(e) 
    pid = events.GenPart_pdgId
    mom = events.GenPart_genPartIdxMother
    
    nPhoton = events.nPhoton

    #GenPart 4-Vector
    gpt = events.GenPart_pt 
    geta = events.GenPart_eta
    gphi = events.GenPart_phi
    gm = events.GenPart_mass
    #Reco Photon 4-Vector
    pt = events.Photon_pt
    eta = events.Photon_eta
    phi = events.Photon_phi 
    m = events.Photon_mass
    #print("Next Event")
    print(len(pid),len(pt))
    if nPhoton == 4:
        for i in range(len(pid)):
            photon0 = TLorentzVector()
            photon0.SetPtEtaPhiM(gpt[i],geta[i],gphi[i],gm[i])
            if pid[i] == 22 and pid[mom[i]] == 90000054:
                #print(" Phi->Photon, PT: ", mom[i], gpt[i])
                for j in range(len(pid)):
                    if j >= i:
                        continue
                    if gpt[j] == gpt[i] and mom[i] == mom[j]: #Matching momentum and same Phi. 
                        #print("PT matched: Event, PT, P1, P2",e, gpt[j],i,j)
                        photon1 = TLorentzVector()
                        photon1.SetPtEtaPhiM(gpt[j],geta[j],gphi[j],gm[j])
                        dR = photon1.DeltaR(photon0)
                        h.Fill(dR)

           
x = h.GetXaxis()
FindAndSetMax(h)
x.SetRangeUser(0, 10)
h.Draw()
#c.SetLogx()
c.SaveAs("X300A15/RECOtest.pdf")           
