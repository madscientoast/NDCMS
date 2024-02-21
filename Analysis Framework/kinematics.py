from ROOT import *

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

def PhiETA(pair,index):
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
    return [phi0.Eta(),phi1.Eta()]