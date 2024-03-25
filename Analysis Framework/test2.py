from ROOT import *
from itertools import combinations
from math import floor,sqrt
from fmt import *
from kinematics import *
from pairing import *
from easyhist import *

canv = TCanvas()
xlow = 0.0
xhigh = 1000.0

f = TFile.Open("/project01/ndcms/atownse2/RSTriPhoton/data/NanoAODv9/EGamma_Run2018D-UL2018_MiniAODv2_NanoAODv9-v3_9.root")
h = TH1D("h1", "RECO (dR vs MA) X Mass [Data]", 1000, xlow, xhigh)
h2 = TH1D("h2", "", 1000, xlow, xhigh)
FillHistX(f,h,"dR")
FillHistX(f,h2,"MA")
#FillCompHistX(f,h,h2,"MA")

x = h.GetXaxis()
y = h.GetYaxis()
x.SetTitle("Mass [GeV]")
y.SetTitle("Events")
FindAndSetMax(h)
h.Draw("E")
h2.Draw("E SAME")
h2.SetLineColor(2)


leg = TLegend(0.7,0.7,0.9,0.9)
leg.AddEntry(h,"dR","l")
leg.AddEntry(h2,"MA","l")
leg.Draw()
canv.SetLogx()
canv.SaveAs("XdRvMA.pdf")