import os
from ROOT import TFile, TH1D, TCanvas
from itertools import combinations
from pairing import *
from kinematics import *

def SetupFiles(d):
    x = next(os.walk(d))[2]
    y = []

    for i in x:
        if i.endswith(".root"):
            y.append(i)
    return y 

def LoadFiles(d):
    l = SetupFiles(d)
    f = []
    for i in l:
        s = d + i
        f.append(TFile.Open(s))
    return f

def CreateHist(e,title,low,high):
    h = []
    for i in range(len(e)):
        name = "h" + str(i)
        graph = TH1D(name, title, 100, low, high)
        h.append(graph)
    return h

def Draw(e,h,var):
    for i in range(len(e)):
        ht = var + " >> h" + str(i)
        e[i].Draw(ht)

def FillHist(f,h,method):
    events = f.Events 
    for e in range(0,events.GetEntries()):
        events.GetEntry(e)
        nPhoton = events.nPhoton
        trigger = events.HLT_TriplePhoton_35_35_5_CaloIdLV2_R9IdVL
        pt = events.Photon_pt
        eta = events.Photon_eta
        phi = events.Photon_phi 
        m = events.Photon_mass
        if nPhoton == 4 and trigger == 1:
            #print("New Event", e)
            vec = [[pt[i],eta[i],phi[i],0] for i in range(4)] #Construct all photons
            comb = combinations(vec,2) #Find all possible pairs
            comb2 = uniques(list(combinations(comb,2))) #Get combinations of pairs
            index = ChoosePair(method,comb2) # Send to Pairing algorithm of choice
            # Get Variables we care to plot #
            PhiMasses = PhiMass(comb2,index)
            avgPhi = (PhiMasses[0]+PhiMasses[1])/2
            h.Fill(avgPhi)

def Fill2DHist(f,h,method):
    events = f.Events 
    for e in range(0,events.GetEntries()):
        events.GetEntry(e)
        nPhoton = events.nPhoton
        pt = events.Photon_pt
        eta = events.Photon_eta
        phi = events.Photon_phi 
        m = events.Photon_mass
        if nPhoton == 4:
            print("New Event", e)
            vec = [[pt[i],eta[i],phi[i],0] for i in range(4)] #Construct all photons
            comb = combinations(vec,2) #Find all possible pairs
            comb2 = uniques(list(combinations(comb,2))) #Get combinations of pairs
            index = ChoosePair(method,comb2) # Send to Pairing algorithm of choice
            # Get Variables we care to plot #
            PhiMasses = PhiMass(comb2,index)
            PhiPTs = PhiPT(comb2,index)
            avgPhi = (PhiMasses[0]+PhiMasses[1])/2
            avgPT = (PhiPTs[0]+PhiPTs[1])/2
            h.Fill(avgPhi,avgPT)

def Render(h,c):
    for i in range(len(h)):
        h[i].SetLineColor(i+1)

        if(i == 0):
            x = h[i].GetXaxis()
            x.SetRange(0, 10)
            h[i].SetMaximum(15000)
            h[i].Draw()
        else:
            h[i].Draw("SAME")
    c.Update()