from ROOT import TFile, TLorentzVector, TCanvas, TH1D
from itertools import combinations
from more_itertools import unique_everseen
from math import floor

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
h = TH1D("h1", "dR [X300A15]", 100, 0.0, 7.0)
f = TFile.Open("X300A15/7F4DE753-B11F-B445-A7FE-C0E7728CE935.root")
events = f.Events

def uniques(lst):
    newlst=[sub[0]+sub[1] for sub in lst] #Flattens list
    res = []
    #This filters out bad combinations
    for i in newlst:
        flag = False
        for j in i:
            if i.count(j) > 1:
                flag = True
        if flag is False:
            res.append(i)
    newlst = [[[r[0],r[1]],[r[2],r[3]]]for r in res] #put back into pairs
    return (newlst)

def PairDeltaR(pair):
    #Divide into pairs of two
    jetA = pair[0]
    jetB = pair[1]
    #Make 4-vectors for all photons in pairs
    photon0 = TLorentzVector()
    photon1 = TLorentzVector()
    photon2 = TLorentzVector()
    photon3 = TLorentzVector()
    photon0.SetPtEtaPhiM(jetA[0][0],jetA[0][1],jetA[0][2],jetA[0][3])
    photon1.SetPtEtaPhiM(jetA[1][0],jetA[1][1],jetA[1][2],jetA[1][3])
    photon2.SetPtEtaPhiM(jetB[0][0],jetB[0][1],jetB[0][2],jetB[0][3])
    photon3.SetPtEtaPhiM(jetB[1][0],jetB[1][1],jetB[1][2],jetB[1][3])
    #Calculate dR
    dR1 = photon1.DeltaR(photon0)
    dR2 = photon3.DeltaR(photon2)
    dR = abs(dR1-0.8)+abs(dR2-0.8) #Quoted from paper
    return dR

#Main Part#
for e in range(0,events.GetEntries()):
    events.GetEntry(e)
    nPhoton = events.nPhoton
    pt = events.Photon_pt
    eta = events.Photon_eta
    phi = events.Photon_phi 
    m = events.Photon_mass
    if nPhoton == 4:
        print("New Event", e)
        vec = [[pt[i],eta[i],phi[i],m[i]] for i in range(4)] #Construct all photons
        comb = unique_everseen(combinations(vec,2)) #Find all possible pairs
        comb2 = uniques(list(unique_everseen(combinations(comb,2)))) #Get combinations of pairs
        dR = [PairDeltaR(c) for c in comb2] #Calculate dR for all combinations
        index = dR.index(min(dR)) #Select the minimum dR from each
        h.Fill(min(dR))

x = h.GetXaxis()
FindAndSetMax(h)
h.Draw()
canv.SaveAs("X300A15/pair_testB.pdf")



        


            

