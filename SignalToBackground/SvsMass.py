from ROOT import *
from itertools import combinations
from math import floor,sqrt
from array import array
from fmt import *
from kinematics import *
from pairing import *
from numpy import arange,around

canv = TCanvas()
#Open Files
signal15 = TFile.Open("X300A15/result.root") #15 GeV MC
signal30 = TFile.Open("X300A30/result.root") #30 GeV MC
signal75 = TFile.Open("X300A75/result.root") #75 GeV MC
signalMassValues = [15.0,30.0,75.0]
signalMasses = std.vector('double')(signalMassValues)
bkg = TFile.Open("/project01/ndcms/atownse2/RSTriPhoton/data/NanoAODv9/EGamma_Run2018D-UL2018_MiniAODv2_NanoAODv9-v3_1.root") #Data File
sig15Events = signal15.Events
sig30Events = signal30.Events
sig75Events = signal75.Events
bkgEvents = bkg.Events
#Select Region
windows = [7.0,23.0,15.0,45.0,62.0,88.0] #windows of analysis [15 GeV, 30 GeV, 75 GeV]
bin_size = 100
#Define Cuts
dr_list = around(arange(0.1,4.1,0.1),1) #same cut list will work for both dr1 and dr2
ma_list = around(arange(0.1,1.1,0.1),1)
dn_list = around(arange(0.1,5.1,0.1),1)

#cuts = [i for i in dr_list]
cuts = [[ma,dn,dr1,dr2] for ma in ma_list for dn in dn_list for dr1 in dr_list for dr2 in dr_list] #All combinations of cuts

#START DEFINING FUNCTIONS############################################################################
def MVAcut(id,v,lst): #90% cut at present
    result = []
    for i in range(len(lst)):
        if v[i] == 1: #Apply electron veto
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
        else:
            continue
    return result

def SavePhotons(events,low,high):
    lst = []
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
            veto = events.Photon_electronVeto
            vec = [[pt[i],eta[i],phi[i],0] for i in range(4)]
            vec = MVAcut(mva,veto,vec) #Apply MVA cut
            if len(vec) < 4:
                continue
            pair = MakePairs(vec)
            index = ChoosePair("dR",pair)
            photon0,photon1,photon2,photon3 = CreatePhotons(pair,index)
            phi0 = photon0+photon1
            phi1 = photon2+photon3
            PhiMasses = [phi0.M(),phi1.M()]
            avgPhi = (PhiMasses[0]+PhiMasses[1])/2
            if avgPhi > low and avgPhi < high:
                lst.append([photon0,photon1,photon2,photon3])
    return lst

def ResizeBkg(list_of_photons,low,high):
    lst = []
    for photons in list_of_photons:
        photon0,photon1,photon2,photon3 = photons[0],photons[1],photons[2],photons[3]
        phi0 = photon0+photon1
        phi1 = photon2+photon3
        PhiMasses = [phi0.M(),phi1.M()]
        avgPhi = (PhiMasses[0]+PhiMasses[1])/2
        if avgPhi > low and avgPhi < high:
            lst.append([photon0,photon1,photon2,photon3])
    return lst


def hfiller(list_of_photons,h,cut):
    for photons in list_of_photons:
        photon0,photon1,photon2,photon3 = photons[0],photons[1],photons[2],photons[3]
        phi0 = photon0+photon1
        phi1 = photon2+photon3
        PhiMasses = [phi0.M(),phi1.M()]
        avgPhi = (PhiMasses[0]+PhiMasses[1])/2
        # Get Values of Variables used for cuts #
        ma = abs(PhiMasses[0]-PhiMasses[1])/(PhiMasses[0]+PhiMasses[1])
        dR1 = photon1.DeltaR(photon0)
        dR2 = photon3.DeltaR(photon2)
        PhiEtas = [phi0.Eta(),phi1.Eta()]
        Etta = abs(PhiEtas[0]-PhiEtas[1])

        #Now evaluate cuts and fill a hist
        if dR1 < cut[3] and dR2 < cut[2] and ma < cut[0] and Etta < cut[1]:
            h.Fill(avgPhi)
    return h

def SigBkg(h1,h2,h3,bins):
    #Take sqrt of b#
    for i in range(bins):
        if (h1.GetBinContent(i)+h2.GetBinContent(i)) == 0:
            h3.SetBinContent(i,0)
        else:
            h3.SetBinContent(i,((h1.GetBinContent(i))/(sqrt(h1.GetBinContent(i)+h2.GetBinContent(i)))))
    return h3

def IterateCuts(sigPhotons,low,high):
    Current_bkgPhotons = ResizeBkg(bkgPhotons,low,high)
    lst = []
    for cut in cuts:
        canv.Clear()
        h1 = TH1D("h1", "Average Mass [MC]", bin_size, low, high)
        h2 = TH1D("h2", "Average Mass [Data]", bin_size, low, high)
        h3 = TH1D("h3", "Sig to Bkg", bin_size, low, high)
        hfiller(sigPhotons,h1,cut)
        hfiller(Current_bkgPhotons,h2,cut)
        SigBkg(h1,h2,h3,bin_size)
        lst.append(h3.Integral()) #Sum of S/sqrt(S+B)
    return lst

def GetCut(cuts,cut_var):
    lst = []
    for cut in cuts:
        if cut_var == "MA":
            lst.append(cut[0])
        if cut_var == "\\Delta \\eta":
            lst.append(cut[1])
        if cut_var == "\\Delta R_1":
            lst.append(cut[2])
        if cut_var == "\\Delta R_2":
            lst.append(cut[3])
    return lst

def PlotCutVsSum(cuts,s,cut_var):
    cut = GetCut(cuts,cut_var)
    CutVsS = TGraph(len(cuts),array('d',cut),array('d',s))
    GraphStyle(CutVsS,cut_var)
    return CutVsS

def PlotCutVsMass(cuts,mass,cut_var):
    CutVsMass = TGraph(3,signalMasses.data(),cuts.data())
    title = "Best Cut vs Signal Mass [" + cut_var + "]"
    CutVsMass.SetTitle("Best Cut vs Signal Mass")
    yax = CutVsMass.GetYaxis()
    xax.SetTitle("Signal Mass [GeV]")
    yax.SetTitle(cut_var)
    CutVsMass.SetMarkerStyle(20)
    CutVsMass.SetMarkerSize(1.5)
    CutVsMass.Draw("ACP")


def MakeAllCuts(cuts,s,mass,base):
    ma_plot = PlotCutVsSum(cuts,s,"MA")
    sub = "MA_" + str(mass) + "GeV.root"
    filename = base+sub
    canv.SaveAs(filename)

    dn_plot = PlotCutVsSum(cuts,s,"\\Delta \\eta")
    sub = "ETA_" + str(mass) + "GeV.root"
    filename = base+sub
    canv.SaveAs(filename)

    dR1_plot = PlotCutVsSum(cuts,s,"\\Delta R_1")
    sub = "DR1_" + str(mass) + "GeV.root"
    filename = base+sub
    canv.SaveAs(filename)
    
    dR2_plot = PlotCutVsSum(cuts,s,"\\Delta R_2")
    sub = "DR2_" + str(mass) + "GeV.root"
    filename = base+sub
    canv.SaveAs(filename)

def GraphStyle(g,cut_var):
    sum_str = "Sum of \\frac{S}{\\sqrt{S+B}}"
    plot_title = "Cut vs Sum [" + cut_var + "]"
    g.SetTitle(plot_title)
    xax = g.GetXaxis()
    yax = g.GetYaxis()
    xax.SetTitle(cut_var)
    yax.SetTitle(sum_str)
    g.SetMarkerStyle(20)
    g.SetMarkerSize(1.5)
    g.Draw("ACP")
    return g

def PrintBest(s,cuts):
    maxS = max(s)
    indexS = s.index(maxS)
    print("Best S is: ", maxS)
    print("The cut index is: ",indexS)
    print("Using the following cuts: ", cuts[indexS])

def DrawBest(s1,s2,s3,cuts,cut_var,base):
    maxS15 = max(s1)
    maxS30 = max(s2)
    maxS75 = max(s3)
    indexS15 = s1.index(maxS15)
    indexS30 = s2.index(maxS30)
    indexS75 = s3.index(maxS75)
    cut = GetCut(cuts,cut_var)
    cut_values = [cut[indexS15],cut[indexS30],cut[indexS75]]
    y = std.vector('double')(cut_values)
    if cut_var == "MA":
        subname = "BestCutsMA.root"
    if cut_var == "\\Delta \\eta":
        subname = "BestCutsETA.root"
    if cut_var == "\\Delta R_1":
        subname = "BestCutsDR1.root"
    if cut_var == "\\Delta R_2":
        subname = "BestCutsDR2.root"
    
    PlotCutVsMass(cut_values,signalMasses,cut_var)
    filename = base+subname 
    canv.SaveAs(filename)
    



#END DEFINING FUNCTIONS##################################################################################
sig15Photons = SavePhotons(sig15Events,windows[0],windows[1])
sig30Photons = SavePhotons(sig30Events,windows[2],windows[3])
sig75Photons = SavePhotons(sig75Events,windows[4],windows[5])
bkgPhotons = SavePhotons(bkgEvents,windows[0],windows[5])
list_of_sigbkg15 = IterateCuts(sig15Photons,windows[0],windows[1])
list_of_sigbkg30 = IterateCuts(sig30Photons,windows[2],windows[3])
list_of_sigbkg75 = IterateCuts(sig75Photons,windows[4],windows[5])

basestr = "06-06-2024/Attempt1/"
cut_var = "\\Delta R_2"
#cut_var = "\\Delta \\eta"
#cut_var = "MA"
sum_str = "Sum of \\frac{S}{\\sqrt{S+B}}"


'''#Old Plot loop
    # 1: For each cut combination make a plot of M vs. Sum#
for i in range(len(cuts)):
    SValues = [list_of_sigbkg15[i],list_of_sigbkg30[i],list_of_sigbkg75[i]]
    S = std.vector('double')(SValues)
    SvsMass = TGraph(3,signalMasses.data(),S.data())
    plot_title = "Sum vs Signal Mass" + "[" + cut_var + " < " + str(cuts[i]) + "]"
    SvsMass.SetTitle(plot_title)
    xax = SvsMass.GetXaxis()
    yax = SvsMass.GetYaxis()
    xax.SetTitle("Signal Mass [GeV]")
    yax.SetTitle(sum_str)
    SvsMass.SetMarkerStyle(20)
    SvsMass.SetMarkerSize(1.5)
    SvsMass.Draw("ACP")
    canv.Update()
    numbercode = str(cuts[i])
    numbercode = numbercode.replace('.','_',1)
    filename = basestr+numbercode+".root"
    canv.SaveAs(filename)'''



# In this sequence make individual plots by signal mass
# 2: Plots of Cut vs Sum #
'''CutVsS15 = TGraph(len(cuts),array('d',cuts),array('d',list_of_sigbkg15))
GraphStyle(CutVsS15,sum_str,cut_var)
subname = "MA_15GeV.root"
filename = basestr+subname
canv.SaveAs(filename)

CutVsS30 = TGraph(len(cuts),array('d',cuts),array('d',list_of_sigbkg30))
GraphStyle(CutVsS30,sum_str,cut_var)
subname = "MA_30GeV.root"
filename = basestr+subname
canv.SaveAs(filename)

CutVsS75 = TGraph(len(cuts),array('d',cuts),array('d',list_of_sigbkg75))
GraphStyle(CutVsS75,sum_str,cut_var)
subname = "MA_75GeV.root"
filename = basestr+subname
canv.SaveAs(filename)'''
MakeAllCuts(cuts,list_of_sigbkg15,15,basestr)
MakeAllCuts(cuts,list_of_sigbkg30,30,basestr)
MakeAllCuts(cuts,list_of_sigbkg75,75,basestr)



'''
# This loop makes plot of total S from summed plots #
# 3: Cut vs Total S
TotalS = []
for i in range(len(cuts)):
    tot = list_of_sigbkg15[i]+list_of_sigbkg30[i]+list_of_sigbkg75[i]
    TotalS.append(tot)

CutvsTotS = TGraph(len(cuts),array('d',cuts),array('d',TotalS))
GraphStyle(CutvsTotS,sum_str,cut_var)
subname = "dR2.root"
filename=basestr+subname
canv.SaveAs(filename)'''

# 4: Plotting just BEST cuts for each mass (need to edit for multiple cuts)
PrintBest(list_of_sigbkg15,cuts)
PrintBest(list_of_sigbkg30,cuts)
PrintBest(list_of_sigbkg75,cuts)
'''Old version
maxS15 = max(list_of_sigbkg15)
maxS30 = max(list_of_sigbkg30)
maxS75 = max(list_of_sigbkg75)
indexS15 = list_of_sigbkg15.index(maxS15)
indexS30 = list_of_sigbkg30.index(maxS30)
indexS75 = list_of_sigbkg75.index(maxS75)
cut_values = [cuts[indexS15],cuts[indexS30],cuts[indexS75]]
y = std.vector('double')(cut_values)
CutVsMass = TGraph(3,signalMasses.data(),y.data())
CutVsMass.SetTitle("Best Cut vs Signal Mass")
xax = CutVsMass.GetXaxis()
yax = CutVsMass.GetYaxis()
xax.SetTitle("Signal Mass [GeV]")
yax.SetTitle("Cut Index")
CutVsMass.SetMarkerStyle(20)
CutVsMass.SetMarkerSize(1.5)
CutVsMass.Draw("ACP")
canv.Update()
filename = basestr+"BestCuts.root"
canv.SaveAs(filename)'''
#New
DrawBest(list_of_sigbkg15,list_of_sigbkg30,list_of_sigbkg75,cuts,"MA",basestr)
DrawBest(list_of_sigbkg15,list_of_sigbkg30,list_of_sigbkg75,cuts,"\\Delta \\eta",basestr)
DrawBest(list_of_sigbkg15,list_of_sigbkg30,list_of_sigbkg75,cuts,"\\Delta \\R_1",basestr)
DrawBest(list_of_sigbkg15,list_of_sigbkg30,list_of_sigbkg75,cuts,"\\Delta \\R_2",basestr)