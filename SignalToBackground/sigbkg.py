from ROOT import *
from itertools import combinations
from math import floor,sqrt
from fmt import *
from kinematics import *
from pairing import *
from numpy import arange

canv = TCanvas()
#Open Files
signal = TFile.Open("X300A30/result.root") #MC
bkg = TFile.Open("/project01/ndcms/atownse2/RSTriPhoton/data/NanoAODv9/EGamma_Run2018D-UL2018_MiniAODv2_NanoAODv9-v3_1.root") #Data File
sigEvents = signal.Events
bkgEvents = bkg.Events
#Select Region
low = 15.0
high = 45.0
bin_size = 100
#Define Cuts
dr1_list = [2.0,2.1,2.2,2.3,2.4,2.5,2.6,2.7,2.8,2.9,3.0]
dr2_list = [3.0,3.1,3.2,3.3]
ma_list = [0.5,0.6,0.7,0.8,0.9,1.0]
dn_list = [4.1,4.2,4.3,4.4,4.5,4.6,4.7,4.8,4.9,5.0]
#cuts = [[i,j,k,l] for i in dr1_list for j in dr2_list for k in ma_list for l in dn_list]
#cuts = [[i,j,k] for i in dr1_list for j in dr2_list for k in ma_list] #Trying without dn cuts
cuts = [i for i in dr1_list]


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
        #if dR1 < cut[0] and dR2 < cut[1] and ma < cut[2] and Etta < cut[3]:
        #if dR1 < cut[0] and dR2 < cut[1] and ma < cut[2]: #Try no Etta
        if dR1 < cut: #only ma
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

sigPhotons = SavePhotons(sigEvents,low,high)
bkgPhotons = SavePhotons(bkgEvents,low,high)

list_of_sigbkg = []
for cut in cuts:
    canv.Clear()
    h1 = TH1D("h1", "Average Mass [MC]", bin_size, low, high)
    h2 = TH1D("h2", "Average Mass [Data]", bin_size, low, high)
    h3 = TH1D("h3", "Sig to Bkg", bin_size, low, high)
    hfiller(sigPhotons,h1,cut)
    hfiller(bkgPhotons,h2,cut)
    SigBkg(h1,h2,h3,bin_size)
    list_of_sigbkg.append(h3.Integral())
    x = h3.GetXaxis()
    y = h3.GetYaxis()
    FindAndSetMax(h3)
    h3.Draw("E")
    basestr = "05-30-2024/Attempt3/"
    #numbercode = str(cut[0]) + "-" + str(cut[1]) + "-" + str(cut[2]) + "-" + str(cut[3])
    #numbercode = str(cut[0]) + "-" + str(cut[1]) + "-" + str(cut[2]) #Try no etta
    numbercode = str(cut)
    #numbercode = numbercode.replace('.','_',4)
    #numbercode = numbercode.replace('.','_',3) #no etta
    numbercode = numbercode.replace('.','_',1)
    filename = basestr+numbercode+".root"
    canv.SaveAs(filename)

maxS = max(list_of_sigbkg)
indexS = list_of_sigbkg.index(maxS)
for s in list_of_sigbkg:
    print("S = ",s)
print("Best S is: ", maxS)
print("The cut index is: ",indexS)
print("Using the following cuts: ", cuts[indexS])
        