from ROOT import *
from itertools import combinations
from math import floor,sqrt
from fmt import *
from kinematics import *
from pairing import *
from easyhist import *

canv = TCanvas()
f = TFile.Open("/project01/ndcms/atownse2/RSTriPhoton/data/NanoAODv9/EGamma_Run2018D-UL2018_MiniAODv2_NanoAODv9-v3_9.root") 
h = TH1D("h1", "RECO (dR) Average Phi Mass [Data]", 100, 0.0, 200.0)
events = f.Events
FillHistNew(f,h,"dR",False,False,"Phi","","AvgMass")

x = h.GetXaxis()
y = h.GetYaxis()
x.SetTitle("Mass [GeV]")
y.SetTitle("Events")
FindAndSetMax(h)
h.Draw("E")
canv.SaveAs("temp6.pdf")