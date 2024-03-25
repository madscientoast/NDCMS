from ROOT import *
from itertools import combinations
from math import floor,sqrt
from fmt import *
from kinematics import *
from pairing import *
from easyhist import *

canv = TCanvas()
xlow = 0.0
xhigh = 500.0

f = TFile.Open("X300A75/result.root")
h = TH1D("h1", "RECO X Mass (dR vs MA) [X300A75]", 1000, xlow, xhigh) #dR
h2 = TH1D("h2", "", 1000, xlow, xhigh) #MA
FillHistX(f,h,"dR")
FillHistX(f,h2,"MA")

x = h.GetXaxis()
y = h.GetYaxis()
x.SetTitle("Mass [GeV]")
y.SetTitle("Events")
FindAndSetMax(h)
h.Draw("E")
h2.Draw("E SAME")
h2.SetLineColor(2)
canv.SaveAs("X300A75/Xmass4.pdf")