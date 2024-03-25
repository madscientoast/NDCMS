from ROOT import *

def CreatePhotons(pair,index):
    diphotonA = pair[index][0]
    diphotonB = pair[index][1]
    photon0 = TLorentzVector()
    photon1 = TLorentzVector()
    photon2 = TLorentzVector()
    photon3 = TLorentzVector()
    photon0.SetPtEtaPhiM(diphotonA[0][0],diphotonA[0][1],diphotonA[0][2],diphotonA[0][3])
    photon1.SetPtEtaPhiM(diphotonA[1][0],diphotonA[1][1],diphotonA[1][2],diphotonA[1][3])
    photon2.SetPtEtaPhiM(diphotonB[0][0],diphotonB[0][1],diphotonB[0][2],diphotonB[0][3])
    photon3.SetPtEtaPhiM(diphotonB[1][0],diphotonB[1][1],diphotonB[1][2],diphotonB[1][3])
    return photon0,photon1,photon2,photon3

def RECOpart(pair,index,part,select,var):
    photon0,photon1,photon2,photon3 = CreatePhotons(pair,index) #Create Photons

    if part == "Phi":
        phi0 = photon0+photon1
        phi1 = photon2+photon3
        if var == "AvgMass":
            return [phi0.M(),phi1.M()]
        if var == "AvgPT":
            return [phi0.Pt(),phi1.Pt()]
        if var == "AvgETA":
            return [phi0.Eta(),phi1.Eta()]
        if var == "dR":
            dR1 = photon1.DeltaR(photon0)
            dR2 = photon3.DeltaR(photon2)
            dR = abs(dR1)+abs(dR2)
            return dR 
    
    if part == "X":
        X = photon0 + photon1 + photon2 + photon3
        if var == "Mass":
            return X.M()

    if part == "Photon":
        if select == "Leading":
            if var == "PT":
                return photon0.Pt()
        if select == "Subleading":
            if var == "PT":
                return photon1.Pt()
        if select == "3rd":
            if var == "PT":
                return photon2.Pt()
        if select == "4th":
            if var == "PT":
                return photon3.Pt() 
