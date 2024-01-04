import os
from ROOT import TFile, TH1D, TCanvas

def SetupFiles(d):
    x = next(os.walk(d))[2]
    y = []

    for i in x:
        if i.endswith(".root"):
            y.append(i)
    return y 

def LoadFiles(d,l):
    f = []
    for i in l:
        s = d + i
        f.append(TFile.Open(s))
    return f

def CreateHist(e,title):
    h = []
    for i in range(len(e)):
        name = "h" + str(i)
        graph = TH1D(name, title, 100, 0.0, 100.0)
        h.append(graph)
    return h

def Draw(e,h,var):
    for i in range(len(e)):
        ht = var + " >> h" + str(i)
        e[i].Draw(ht)

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
