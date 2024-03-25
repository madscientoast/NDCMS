from ROOT import *

f = TFile.Open("/project01/ndcms/atownse2/RSTriPhoton/data/NanoAODv9/EGamma_Run2018D-UL2018_MiniAODv2_NanoAODv9-v3_9.root")
events = f.Events

#events.GetListOfBranches().Print()
#events.Print()
c1 = TCanvas()

'''h = TH1D("h1", "Photon mvaID", 100, -2.0, 2.0)
events.Draw("Photon_mvaID >> h1")
c1.SaveAs("mva_test.pdf")'''

h = TH1D("h1", "Trigger", 100, -2.0, 2.0)
events.Draw("HLT_TriplePhoton_35_35_5_CaloIdLV2_R9IdVL >> h1")
c1.SaveAs("trigger_test.pdf")