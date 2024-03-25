from ROOT import *
from itertools import combinations
from more_itertools import unique_everseen
from math import floor,sqrt

# Function to filter unique combination for diphoton objects in MC #
def uniques(lst):
    pool = (sub[0]+sub[1] for sub in lst)
    res = []
    for i in pool:
        flag = False
        for j in i: 
            if i.count(j) > 1:
                flag = True 
        if flag is False:
            res.append(i)
    return ([[r[0],r[1]],[r[2],r[3]]]for r in res)

# Function to filter unique combination for diphoton objects in MC #
def uniques_old(lst):
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

# Make actual diphoton objects #
def MakePairs(vec):
    nums = [i for i in range(4)]
    com = [sub[0]+sub[1] for sub in uniques(combinations(combinations(nums,2),2))]
    nvec = []
    for i in range(3):
        id = [j for j in com[i]]
        a,b,c,d = id[0],id[1],id[2],id[3]
        nvec.append(([vec[a],vec[b]],[vec[c],vec[d]]))
    return nvec

# Choose Pairing Alg #
def ChoosePair(choice,box):
    if choice == "dR":
        dR = [PairDeltaR(c) for c in box] #Calculate dR for all combinations
        index = dR.index(min(dR)) #Select the minimum dR from each
    if choice == "MA":
        MA = [PairMA(c) for c in box] #Calculate dR for all combinations
        index = MA.index(min(MA)) #Select the minimum dR from each
    return index

def BasePair(pair):
    #Divide into pairs of two
    diphotonA = pair[0]
    diphotonB = pair[1]
    #Make 4-vectors for all photons in pairs
    photon0 = TLorentzVector()
    photon1 = TLorentzVector()
    photon2 = TLorentzVector()
    photon3 = TLorentzVector()
    photon0.SetPtEtaPhiM(diphotonA[0][0],diphotonA[0][1],diphotonA[0][2],diphotonA[0][3])
    photon1.SetPtEtaPhiM(diphotonA[1][0],diphotonA[1][1],diphotonA[1][2],diphotonA[1][3])
    photon2.SetPtEtaPhiM(diphotonB[0][0],diphotonB[0][1],diphotonB[0][2],diphotonB[0][3])
    photon3.SetPtEtaPhiM(diphotonB[1][0],diphotonB[1][1],diphotonB[1][2],diphotonB[1][3])
    return photon0,photon1,photon2,photon3

# Pairing Algorithm using dR #
def PairDeltaR(pair):
    '''#Divide into pairs of two
    diphotonA = pair[0]
    diphotonB = pair[1]
    #Make 4-vectors for all photons in pairs
    photon0 = TLorentzVector()
    photon1 = TLorentzVector()
    photon2 = TLorentzVector()
    photon3 = TLorentzVector()
    photon0.SetPtEtaPhiM(diphotonA[0][0],diphotonA[0][1],diphotonA[0][2],diphotonA[0][3])
    photon1.SetPtEtaPhiM(diphotonA[1][0],diphotonA[1][1],diphotonA[1][2],diphotonA[1][3])
    photon2.SetPtEtaPhiM(diphotonB[0][0],diphotonB[0][1],diphotonB[0][2],diphotonB[0][3])
    photon3.SetPtEtaPhiM(diphotonB[1][0],diphotonB[1][1],diphotonB[1][2],diphotonB[1][3])'''
    photon0,photon1,photon2,photon3 = BasePair(pair)
    #Calculate dR
    dR1 = photon1.DeltaR(photon0)
    dR2 = photon3.DeltaR(photon2)
    #dR = abs(dR1-0.8)+abs(dR2-0.8) #Quoted from paper
    dR = abs(dR1)+abs(dR2)
    return dR

# Pairing Algorithm using Mass Asymmetry #
def PairMA(pair):
    #Divide into pairs of two
    diphotonA = pair[0]
    diphotonB = pair[1]
    #Make 4-vectors for all photons in pairs
    photon0 = TLorentzVector()
    photon1 = TLorentzVector()
    photon2 = TLorentzVector()
    photon3 = TLorentzVector()
    photon0.SetPtEtaPhiM(diphotonA[0][0],diphotonA[0][1],diphotonA[0][2],diphotonA[0][3])
    photon1.SetPtEtaPhiM(diphotonA[1][0],diphotonA[1][1],diphotonA[1][2],diphotonA[1][3])
    photon2.SetPtEtaPhiM(diphotonB[0][0],diphotonB[0][1],diphotonB[0][2],diphotonB[0][3])
    photon3.SetPtEtaPhiM(diphotonB[1][0],diphotonB[1][1],diphotonB[1][2],diphotonB[1][3])
    #Calculate Mass Asym

    phi0 = photon0+photon1
    phi1 = photon2+photon3 
    ma = (phi0.M()-phi1.M())/(phi0.M()+phi1.M()) 
    return ma