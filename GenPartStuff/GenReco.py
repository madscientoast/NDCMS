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
            if pid[i] == 22 and pid[mom[i]] == 90000054: #Make sure we have photons and they are from Phi
                #print(" Phi->Photon, PT: ", mom[i], gpt[i])
                for j in range(len(pid)):
                    if j >= i:
                        continue
                    if mom[i] == mom[j]: #Make sure ALL photons are from same mother
                        print("Matched mother: Event",e) 
                        print("GEN: ", gpt[i],geta[i],gphi[i]) #Inspecting PT, ETA, and PHI for GenPart and RECO photons. 
                        print("GEN: ", gpt[j],geta[j],gphi[j])
                        GenPart0 = TLorentzVector()
                        GenPart1 = TLorentzVector()
                        GenPart0.SetPtEtaPhiM(gpt[i],geta[i],gphi[i],gm[i])
                        GenPart1.SetPtEtaPhiM(gpt[j],geta[j],gphi[j],gm[j])
                        dR1=[] 
                        dR2=[]
                        #Match GenPart to RECO photons
                        for k in range(len(pt)):
                            photon0 = TLorentzVector()
                            photon0.SetPtEtaPhiM(pt[k],eta[k],phi[k],m[k])
                            dR1.append(GenPart0.DeltaR(photon0))
                            dR2.append(GenPart1.DeltaR(photon0))
                        #Minimize dR
                        index1 = dR1.index(min(dR1))
                        index2 = dR2.index(min(dR2))
                        print("RECO: ",pt[index1],eta[index1],phi[index1]) #We indeed get 4 photons per event
                        print("RECO: ",pt[index2],eta[index2],phi[index2]) #(as pairs of two at a time)
    

               
