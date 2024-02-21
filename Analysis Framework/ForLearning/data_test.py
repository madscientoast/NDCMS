from ROOT import *

f = TFile.Open("/project01/ndcms/atownse2/RSTriPhoton/data/NanoAODv9/DoubleEG_Run2016B-ver1_HIPM_UL2016_MiniAODv2_NanoAODv9-v2_1.root")
events = f.Events

#events.GetListOfBranches().Print()
c1 = TCanvas()

h = TH1D("h1", "nPhoton", 10, 0.0, 10.0)
events.Draw("nPhoton >> h1")
c1.SaveAs("data_test.pdf")