from ROOT import TFile, TLorentzVector

f = TFile.Open("X300A15/7F4DE753-B11F-B445-A7FE-C0E7728CE935.root")
events = f.Events

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
    #RECO Photon 4-Vector
    pt = events.Photon_pt
    eta = events.Photon_eta
    phi = events.Photon_phi 
    m = events.Photon_mass
    if nPhoton >= 4: #Make sure there are 4 photons in the event
        for i in range(len(pid)):
            if pid[i] == 22 and pid[mom[i]] == 90000054:
                #print(" Phi->Photon, PT: ", mom[i], gpt[i])
                for j in range(len(pid)):
                    if j >= i:
                        continue
                    if gpt[j] == gpt[i] and mom[i] == mom[j]:
                        print("PT matched: Event, PT, P1, P2, momID1, momID2 ",e, gpt[j],i,j,mom[i], mom[j],pid[mom[j]]) 
                        #Only 1 pair of same GenPart PT in a event at a time?
                        print("GEN: ", gpt[i],geta[i],gphi[i]) #Inspecting PT, ETA, and PHI for GenPart and RECO photons. 
                        print("GEN: ", gpt[j],geta[j],gphi[j])
                        GenPart0 = TLorentzVector()
                        GenPart1 = TLorentzVector()
                        GenPart0.SetPtEtaPhiM(gpt[i],geta[i],gphi[i],gm[i])
                        GenPart1.SetPtEtaPhiM(gpt[j],geta[j],gphi[j],gm[j])
                        for k in range(len(pt)):
                            photon0 = TLorentzVector()
                            photon0.SetPtEtaPhiM(pt[k],eta[k],phi[k],m[k])
                            dR1 = GenPart0.DeltaR(photon0) 
                            dR2 = GenPart1.DeltaR(photon0)
                            #print("RECO: ",pt[k],eta[k],phi[k],dR1,dR2)
                            if dR1 < 0.7 and dR2 < 0.7: #Still need to fine tune a bit
                                print("RECO: ",pt[k],eta[k],phi[k],dR1,dR2) #This matches GenPart to RECO I think? I'll ask later. 
                            
    

               
