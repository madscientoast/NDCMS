from ROOT import TFile, TLorentzVector

f = TFile.Open("X300A15/8FC216FE-6399-6845-8572-36A5078139F1.root")
events = f.Events

for e in range(events.GetEntries()):
    events.GetEntry(e) 
    pid = events.GenPart_pdgId
    mom = events.GenPart_genPartIdxMother
    m = events.GenPart_mass
    nPhoton = events.nPhoton
    print("Next Event")
    if nPhoton == 4:
        for i in range(len(pid)):
            if pid[i] == 22 and pid[mom[i]] == 90000054:
                print(" Phi->Photon, Event: ", mom[i], e)
            
        
    