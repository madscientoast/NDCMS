import os
from ROOT import TFile, TH1D, TH2D, TCanvas
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

def CreateHist(bins,str,source,type):
    if str == "AvgPhiMass":
        hname = "RECO " +"("+type+") Average Phi Mass [" +source+"]"
        return TH1D("h1", hname, bins, 0, 200)
    if str == "4mass":
        hname = "RECO " +"("+type+") 4-Mass [" +source+"]"
        return TH1D("h1", hname, bins, 0, 200)

def Create2DHist(bins,str,source,type):
    if str =="AvgMass vs AvgPT":
        hname = "RECO " +"("+type+") Average Phi Mass vs Average Phi PT [" +source+"]"
        return TH2D("h1", hname, bins, 0.0, 200.0,bins,0.0,300.0)
    if str =="AvgMass vs AvgETA":
        hname = "RECO " +"("+type+") Average Phi Mass vs Average Phi ETA [" +source+"]"
        TH2D("h1", hname, bins, 0.0, 200.0, bins, -2.0, 2.0)
    if str == "Mass1 vs Mass2":
        hname = "RECO " +"("+type+") Mass 1 vs Mass 2 [" +source+"]"
        return TH2D("h1", hname, bins, 0.0, 200.0,bins,0.0,200.0)
    if str == "AvgMass vs 4Mass":
        hname = "RECO " +"("+type+") Average Phi Mass vs 4-mass [" +source+"]"
        return TH2D("h1", "RECO (dR) Average Phi Mass vs 4-mass [Data]", 5*bins, 0.0, 5000.0,bins,0.0,200.0)
    if str == "AvgMass vs LeadingPT":
        hname = "RECO " +"("+type+") Average Phi Mass vs Leading PT [" +source+"]"
        return TH2D("h1", hname, bins, 0.0, 200.0,bins,0.0,300.0)
    if str == "AvgMass vs SubPT":
        hname = "RECO " +"("+type+") Average Phi Mass vs Subleading PT [" +source+"]"
        return TH2D("h1", hname, bins, 0.0, 200.0,bins,0.0,300.0)
    if str == "AvgMass vs 4thPT":
        hname = "RECO " +"("+type+") Average Phi Mass vs 4th PT [" +source+"]"
        return TH2D("h1", hname, bins, 0.0, 200.0,bins,0.0,300.0)
    if str == "AvgMass vs MAsym":
        hname = "RECO " +"("+type+") Average Phi Mass vs Mass Asymmetry [" +source+"]"
        return TH2D("h1", hname, bins, 0.0, 200.0,100,-1.0,1.0)
    if str == "AvgMass vs dR":
        #hname = "RECO " +"("+type+") Average Phi Mass vs dR [" +source+"]"
        hname = "RECO " +"("+type+") Mass Ratio vs dR [" +source+"]"
        return TH2D("h1", hname, bins, 0.0, 1.0,100,-4.0,4.0)



def CreateHistList(e,title,low,high):
    h = []
    for i in range(len(e)):
        name = "h" + str(i)
        graph = TH1D(name, title, 100, low, high)
        h.append(graph)
    return h


def DrawList(e,h,var):
    for i in range(len(e)):
        ht = var + " >> h" + str(i)
        e[i].Draw(ht)

def MVAcut(id,lst): #90% cut at present
    result = []
    for i in range(len(lst)):
        if lst[i][1] > 1.4: #Check eta to see if in endcap
            if id[i] > 0.14: #apply endcap cut
                continue
            else:
                result.append(lst[i])
        else: #in barrel
            if id[i] > 0.27: #apply barrel cut
                continue
            else:
                result.append(lst[i])
    return result

def MVAcutFail(id,lst): #90% cut at present
    result = []
    for i in range(len(lst)):
        if lst[i][1] > 1.4: #Check eta to see if in endcap
            if id[i] > 0.14: #apply endcap cut
                result.append(lst[i])
            else:
                continue
        else: #in barrel
            if id[i] > 0.27: #apply barrel cut
                result.append(lst[i])
            else:
                continue
    return result

def FillHistNew(f,h,method,isMC,is2D,part,select,var):
    events = f.Events 
    for e in range(0,events.GetEntries()): 
        events.GetEntry(e)
        nPhoton = events.nPhoton
        trigger = events.HLT_TriplePhoton_35_35_5_CaloIdLV2_R9IdVL
        if nPhoton == 4 and trigger == 1:
            pt = events.Photon_pt
            eta = events.Photon_eta
            phi = events.Photon_phi 
            m = events.Photon_mass
            mva = events.Photon_mvaID
            vec = [[pt[i],eta[i],phi[i],0] for i in range(4)]
            if isMC == False:
                vec = MVAcut(mva,vec) #Apply MVA cut
                if len(vec) < 4:
                    continue
                #comb = combinations(vec,2) #Find all possible pairs
                #comb2 = uniques_old(list(combinations(comb,2))) #Get combinations of pairs
                comb2 = MakePairs(vec)
                index = ChoosePair(method,comb2)
                if is2D == True:
                    Fill2D(h,comb2,index,part,select,var) 
                else:
                    if pt[0] > 90.0: #basically testing a stricter trigger
                        Fill1D(h,comb2,index,part,select,var)
            else:
                #comb = combinations(vec,2) #Find all possible pairs
                #comb2 = uniques_old(list(combinations(comb,2))) #Get combinations of pairs
                comb2 = MakePairs(vec)
                index = ChoosePair(method,comb2)
                if is2D == True:
                    Fill2D(h,comb2,index,part,select,var)
                else:
                    Fill1D(h,comb2,index,part,select,var) 

def Fill1D(h,comb,index,part,select,var):
    if part == "Phi":
        if var == "AvgMass":
            PhiMasses = RECOpart(comb,index,part,select,var)
            avgPhi = (PhiMasses[0]+PhiMasses[1])/2
            h.Fill(avgPhi)
        if var == "AvgPT":
            PhiPTs = RECOpart(comb,index,part,select,var)
            avgPT = (PhiPTs[0]+PhiPTs[1])/2
            h.Fill(avgPT)
        if var == "AvgETA":
            PhiETA = RECOpart(comb,index,part,select,var)
            avgETA = (PhiETAs[0]+PhiETAs[1])/2
            h.Fill(avgETA)
    if part == "X":
        if var == "Mass":
            Xm = RECOpart(comb,index,part,select,var)
            h.Fill(Xm)

def Fill2D(h,comb,index,part,select,str):
    if str =="AvgMass vs AvgPT":
        PhiMasses = RECOpart(comb,index,"Phi",select,"AvgMass")
        PhiPTs = RECOpart(comb,index,"Phi",select,"AvgPT")
        avgPhi = (PhiMasses[0]+PhiMasses[1])/2
        avgPT = (PhiPTs[0]+PhiPTs[1])/2
        h.Fill(avgPhi,avgPT)
    if str =="AvgMass vs AvgETA":
        PhiMasses = RECOpart(comb,index,"Phi",select,"AvgMass")
        PhiETAs = RECOpart(comb,index,"Phi",select,"AvgETA")
        avgPhi = (PhiMasses[0]+PhiMasses[1])/2
        avgETA = (PhiETAs[0]+PhiETAs[1])/2
        h.Fill(avgPhi,avgETA)
    if str == "Mass1 vs Mass2":
        PhiMasses = RECOpart(comb,index,"Phi",select,"AvgMass")
        h.Fill(PhiMasses[0],PhiMasses[1])
    if str == "AvgMass vs 4Mass":
        PhiMasses = RECOpart(comb,index,"Phi",select,"AvgMass")
        avgPhi = (PhiMasses[0]+PhiMasses[1])/2
        Xm = RECOpart(comb,index,"X",select,"Mass")
        h.Fill(Xm,avgPhi)
    if str == "AvgMass vs LeadingPT":
        PhiMasses = RECOpart(comb,index,"Phi",select,"AvgMass")
        avgPhi = (PhiMasses[0]+PhiMasses[1])/2
        PhotoPT = RECOpart(comb,index,"Photon",select,"PT")
        h.Fill(avgPhi,PhotoPT)
    if str == "AvgMass vs SubPT":
        PhiMasses = RECOpart(comb,index,"Phi",select,"AvgMass")
        avgPhi = (PhiMasses[0]+PhiMasses[1])/2
        PhotoPT = RECOpart(comb,index,"Photon",select,"PT")
        h.Fill(avgPhi,PhotoPT)
    if str == "AvgMass vs 4thPT":
        PhiMasses = RECOpart(comb,index,"Phi",select,"AvgMass")
        avgPhi = (PhiMasses[0]+PhiMasses[1])/2
        PhotoPT = RECOpart(comb,index,"Photon",select,"PT")
        h.Fill(avgPhi,PhotoPT)
    if str == "AvgMass vs MAsym":
        PhiMasses = RECOpart(comb,index,"Phi",select,"AvgMass")
        avgPhi = (PhiMasses[0]+PhiMasses[1])/2
        ma = (PhiMasses[0]-PhiMasses[1])/(PhiMasses[0]+PhiMasses[1]) 
        h.Fill(avgPhi,ma)
    if str == "AvgMass vs dR":
        PhiMasses = RECOpart(comb,index,"Phi",select,"AvgMass")
        avgPhi = (PhiMasses[0]+PhiMasses[1])/2
        Xm = RECOpart(comb,index,"X",select,"Mass")
        dR = RECOpart(comb,index,"Phi",select,"dR")
        ratio = avgPhi/Xm
        h.Fill(ratio,dR)

def FillHist(f,h,method):
    events = f.Events 
    for e in range(0,events.GetEntries()): 
        events.GetEntry(e)
        nPhoton = events.nPhoton
        trigger = events.HLT_TriplePhoton_35_35_5_CaloIdLV2_R9IdVL
        if nPhoton == 4 and trigger == 1:
            pt = events.Photon_pt
            eta = events.Photon_eta
            phi = events.Photon_phi 
            m = events.Photon_mass
            mva = events.Photon_mvaID
            vec = [[pt[i],eta[i],phi[i],0] for i in range(4)] #Construct all photons
            vec = MVAcut(mva,vec) #Apply MVA cut
            if len(vec) < 4:
                continue
            else:
                comb = combinations(vec,2) #Find all possible pairs
                comb2 = uniques(list(combinations(comb,2))) #Get combinations of pairs
                index = ChoosePair(method,comb2) # Send to Pairing algorithm of choice
                # Get Variables we care to plot #
                PhiMasses = PhiMass(comb2,index)
                PhiPTs = PhiPT(comb2,index)
                PhiETAs = PhiETA(comb2,index)
                avgPhi = (PhiMasses[0]+PhiMasses[1])/2
                avgETA = (PhiETAs[0]+PhiETAs[1])/2
                avgPT = (PhiPTs[0]+PhiPTs[1])/2
                h.Fill(avgPhi)

def Fill2DHist(f,h,method):
    events = f.Events 
    for e in range(0,events.GetEntries()):
        events.GetEntry(e)
        nPhoton = events.nPhoton
        trigger = events.HLT_TriplePhoton_35_35_5_CaloIdLV2_R9IdVL
        #if nPhoton == 4:
        if nPhoton == 4 and trigger == 1:
            pt = events.Photon_pt
            eta = events.Photon_eta
            phi = events.Photon_phi 
            m = events.Photon_mass
            mva = events.Photon_mvaID
            vec = [[pt[i],eta[i],phi[i],0] for i in range(4)] #Construct all photons
            vec = MVAcut(mva,vec) #Apply MVA cut
            if len(vec) < 4:
                continue
            else:
                comb = combinations(vec,2) #Find all possible pairs
                comb2 = uniques(list(combinations(comb,2))) #Get combinations of pairs
                index = ChoosePair(method,comb2) # Send to Pairing algorithm of choice
                # Get Variables we care to plot #
                PhiMasses = PhiMass(comb2,index)
                PhiPTs = PhiPT(comb2,index)
                avgPhi = (PhiMasses[0]+PhiMasses[1])/2
                avgPT = (PhiPTs[0]+PhiPTs[1])/2
                PhiETAs = PhiETA(comb2,index)
                avgETA = (PhiETAs[0]+PhiETAs[1])/2
                Xm = XMass(comb2,index)
                #h.Fill(Xm,avgPhi)
                h.Fill(avgPhi,avgETA)
            #h.Fill(PhiMasses[0],PhiMasses[1]) #Plot Mass1 vs Mass2

def FillCompHist(f,h,h2,method):
    events = f.Events 
    for e in range(0,events.GetEntries()):
        events.GetEntry(e)
        nPhoton = events.nPhoton
        trigger = events.HLT_TriplePhoton_35_35_5_CaloIdLV2_R9IdVL
        if nPhoton == 4:
            pt = events.Photon_pt
            eta = events.Photon_eta
            phi = events.Photon_phi 
            m = events.Photon_mass
            vec = [[pt[i],eta[i],phi[i],0] for i in range(4)] #Construct all photons
            comb = combinations(vec,2) #Find all possible pairs
            comb2 = uniques(list(combinations(comb,2))) #Get combinations of pairs
            index = ChoosePair(method,comb2) # Send to Pairing algorithm of choice
            # Get Variables we care to plot #
            PhiMasses = PhiMass(comb2,index)
            avgPhi = (PhiMasses[0]+PhiMasses[1])/2
            h.Fill(avgPhi)
            if trigger == 1:
                h2.Fill(avgPhi)


def FillCompHistX(f,h,h2,method):
    events = f.Events 
    for e in range(0,events.GetEntries()):
        events.GetEntry(e)
        nPhoton = events.nPhoton
        trigger = events.HLT_TriplePhoton_35_35_5_CaloIdLV2_R9IdVL
        if nPhoton == 4:
            pt = events.Photon_pt
            eta = events.Photon_eta
            phi = events.Photon_phi 
            m = events.Photon_mass
            vec = [[pt[i],eta[i],phi[i],0] for i in range(4)] #Construct all photons
            comb = combinations(vec,2) #Find all possible pairs
            comb2 = uniques(list(combinations(comb,2))) #Get combinations of pairs
            index = ChoosePair(method,comb2) # Send to Pairing algorithm of choice
            # Get Variables we care to plot #
            Xm = XMass(comb2,index)
            h.Fill(Xm)
            if trigger == 1:
                h2.Fill(Xm)

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