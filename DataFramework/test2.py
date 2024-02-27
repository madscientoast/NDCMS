from ROOT import *
from itertools import combinations
from math import floor,sqrt
from fmt import *
from kinematics import *
from pairing import *
from easyhist import *

canv = TCanvas()
xlow = 0.0
xhigh = 200.0

f = TFile.Open("/project01/ndcms/atownse2/RSTriPhoton/data/NanoAODv9/EGamma_Run2018D-UL2018_MiniAODv2_NanoAODv9-v3_9.root")
h = TH1D("h1", "RECO (dR) Average Phi Mass [Data]", 1000, 0.0, 200.0)
FillHist(f,h,"dR")

x = h.GetXaxis()
y = h.GetYaxis()
x.SetTitle("Mass [GeV]")
y.SetTitle("Events")
FindAndSetMax(h)
h.Draw("E")
canv.SetLogx()
canv.SaveAs("TriggerDataTestDR3.pdf")