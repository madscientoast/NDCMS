from ROOT import TFile, TLorentzVector, TCanvas, TH1D, TF1
from ROOT import gStyle as gs 
from itertools import combinations
from more_itertools import unique_everseen
from math import floor

gs.SetOptStat(000000000)
gs.SetOptFit(1)

def FindAndSetMax(h): #Marc's code
	maximum = 0.0
	#h.SetStats(0)
	t = h.GetMaximum()
	if t > maximum:
		maximum = t
	h.GetYaxis().SetRangeUser(0,maximum*1.35)#should be 1.35 (below as well)
	h.SetLineWidth(2)
	return maximum*1.35

canv = TCanvas()
h = TH1D("h1", "RECO (MA) Average PT [X3000A750]", 100, 0, 2000)
#h = TH1D("h1", "Mass Asymmetry [X300A15]", 100, -1.0, 1.0)
f = TFile.Open("X3000A750/3A3C76AE-9E9D-5545-8A4C-B4E443FE2F36.root")
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

def PairMA(pair):
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
    #Calculate Mass Asym

    phi0 = photon0+photon1
    phi1 = photon2+photon3 
    ma = (phi0.M()-phi1.M())/(phi0.M()+phi1.M()) 
    return ma

def PhiMass(pair,index):
    jetA = pair[index][0]
    jetB = pair[index][1]
    photon0 = TLorentzVector()
    photon1 = TLorentzVector()
    photon2 = TLorentzVector()
    photon3 = TLorentzVector()
    photon0.SetPtEtaPhiM(jetA[0][0],jetA[0][1],jetA[0][2],jetA[0][3])
    photon1.SetPtEtaPhiM(jetA[1][0],jetA[1][1],jetA[1][2],jetA[1][3])
    photon2.SetPtEtaPhiM(jetB[0][0],jetB[0][1],jetB[0][2],jetB[0][3])
    photon3.SetPtEtaPhiM(jetB[1][0],jetB[1][1],jetB[1][2],jetB[1][3])
    phi0 = photon0+photon1
    phi1 = photon2+photon3 
    return [phi0.M(),phi1.M()]

def PhiPT(pair,index):
    jetA = pair[index][0]
    jetB = pair[index][1]
    photon0 = TLorentzVector()
    photon1 = TLorentzVector()
    photon2 = TLorentzVector()
    photon3 = TLorentzVector()
    photon0.SetPtEtaPhiM(jetA[0][0],jetA[0][1],jetA[0][2],jetA[0][3])
    photon1.SetPtEtaPhiM(jetA[1][0],jetA[1][1],jetA[1][2],jetA[1][3])
    photon2.SetPtEtaPhiM(jetB[0][0],jetB[0][1],jetB[0][2],jetB[0][3])
    photon3.SetPtEtaPhiM(jetB[1][0],jetB[1][1],jetB[1][2],jetB[1][3])
    phi0 = photon0+photon1
    phi1 = photon2+photon3 
    return [phi0.Pt(),phi1.Pt()]
    

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
        #vec = [[pt[i],eta[i],phi[i],m[i]] for i in range(4)] #Construct all photons
        vec = [[pt[i],eta[i],phi[i],0] for i in range(4)] #Construct all photons
        comb = combinations(vec,2) #Find all possible pairs
        comb2 = uniques(list(combinations(comb,2))) #Get combinations of pairs
        MA = [PairMA(c) for c in comb2] #Calculate MA for all combinations
        index = MA.index(min(MA)) #Select the minimum MA from each
        PhiMasses = PhiMass(comb2,index)
        PhiPts = PhiPT(comb2,index)
        avgPhi = (PhiMasses[0]+PhiMasses[1])/2
        avgPT = (PhiPts[0]+PhiPts[1])/2
        #h.Fill(avgPhi)
        #h.Fill(min(MA))
        if avgPhi > 800.0:
            h.Fill(avgPT)


x = h.GetXaxis()
y = h.GetYaxis()
x.SetTitle("Mass [GeV]")
#y.SetRangeUser(0,1000)
#x.SetRangeUser(-0.2,0.2)
y.SetTitle("Events")
FindAndSetMax(h)
h.Draw()
#cfit = TF1("cfit","crystalball")
#h.Fit("gaus")
#h.Fit(cfit)
canv.SaveAs("X3000A750/MAtails.pdf")
#canv.SaveAs("X300A15/MAsym_test2.pdf")


            

