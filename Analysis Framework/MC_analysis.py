from ROOT import *
from itertools import combinations
from more_itertools import unique_everseen
from math import floor,sqrt
from fmt import *
from kinematics import *
from pairing import *


canv = TCanvas()
pad1 = TPad("pad1", "tall",0,0.25,1,1)
pad2 = TPad("pad2", "short",0,0.0,1.0,0.3)
zline = TLine(50.0,0.0,100.0,0.0)
pad2.SetBottomMargin(0.35)
h = TH1D("h1", "RECO (dR) Average Phi Mass [X300A75]", 100, 50.0, 100.0)
f = TFile.Open("X300A75/3B7E2B81-FCBB-F040-B6B2-C71D818DC066.root") #big file
events = f.Events

#Main Part#
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
        index = ChoosePair("dR",comb2) # Send to Pairing algorithm of choice
        # Get Variables we care to plot #
        PhiMasses = PhiMass(comb2,index)
        avgPhi = (PhiMasses[0]+PhiMasses[1])/2
        h.Fill(avgPhi)

pad1.cd()
x = h.GetXaxis()
y = h.GetYaxis()
x.SetTitle("Mass [GeV]")
y.SetTitle("Events")
FindAndSetMax(h)
h.GetXaxis().SetLabelSize(0)
h.Draw("E")
cb = FitCB(h,75.0,1.94)
#cb = FitCB(h,70.0,-2.3) #Fit for X300A75
cb.Draw("SAME")
cb.SetLineColor(2)
pad2.cd()
h3 = PullPlot(h,cb)
h3.Draw("E")
zline.SetLineColor(2)
zline.Draw("SAME")
canv.cd()
pad1.Draw()
pad2.Draw()
canv.SaveAs("X300A75/test.pdf")
