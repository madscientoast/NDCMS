from ROOT import *
from itertools import combinations
from more_itertools import unique_everseen
from math import floor,sqrt

# Function to filter unique combination for dijets in MC #
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

# Choose Pairing Alg #
def ChoosePair(choice,box):
    if choice == "dR":
        dR = [PairDeltaR(c) for c in box] #Calculate dR for all combinations
        index = dR.index(min(dR)) #Select the minimum dR from each
    if choice == "MA":
        MA = [PairMA(c) for c in box] #Calculate dR for all combinations
        index = MA.index(min(MA)) #Select the minimum dR from each
    return index

# Pairing Algorithm using dR #
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

# Pairing Algorithm using Mass Asymmetry #
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