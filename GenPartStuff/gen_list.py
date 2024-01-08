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
                        for k in range(len(pt)):
                            #print("RECO: ",pt[k],eta[k],phi[k])
                            if abs(geta[i]-eta[k]) < 0.2 or abs(geta[j]-eta[k]) < 0.2: #ROUGH but will refine
                                if abs(gphi[i]-phi[k]) < 0.2 or abs(gphi[j]-phi[k]) < 0.2:
                                    print("RECO: ",pt[k],eta[k],phi[k])                 #seems to work for matching GenPart to RECO, will ask later
                            
    

               
