from ROOT import *
from itertools import combinations
from math import floor,sqrt
from fmt import *
from kinematics import *
from pairing import *
from easyhist import *

canv = TCanvas()
#Open Files and Create Histograms
f = TFile.Open("/project01/ndcms/atownse2/RSTriPhoton/data/NanoAODv9/EGamma_Run2018D-UL2018_MiniAODv2_NanoAODv9-v3_9.root")
h = Create2DHist(1000,"AvgMass vs dR","Data","dR")

#Fill Histograms
FillHistNew(f,h,"dR",False,True,"Phi","","AvgMass vs dR")

#Drawing Time
x = h.GetXaxis()
y = h.GetYaxis()
z = h.GetZaxis()
x.SetTitle("Average Mass/4-mass")
y.SetTitle("dR")
z.SetTitle("Events")
FindAndSetMax(h)
h.Draw("colz")
#canv.SetLogx()
canv.SaveAs("MassRatioVsdR.pdf")
canv.SaveAs("MassRatioVsdR.root")