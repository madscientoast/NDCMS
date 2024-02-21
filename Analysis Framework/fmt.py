from ROOT import *
from ROOT import gStyle as gs

gs.SetOptStat(000000000)
gs.SetOptFit(1)

def FindAndSetMax(h): #Marc's code
	maximum = 0.0
	#h.SetStats(0)
	t = h.GetMaximum()
	if t > maximum:
		maximum = t
	h.GetYaxis().SetRangeUser(0,maximum*1.35)#should be 1.35 (below as well)
	h.SetLineWidth(2)
	return maximum*1.35

def FitCB(h,stdev,alpha):
	cfit = TF1("cfit","crystalball",40.0,90.0)
	cfit.SetParameter(2,stdev)
	#cfit.SetParameter(3,alpha)
	h.Fit(cfit,"EMR0")
	#cfit.Draw("SAME")
	#cfit.SetLineColor(2)
	return cfit

def PullPlot(h,cb):
	sh = TH1D("sh", "", 100, 40.0, 90)
	h2 = cb.GetHistogram() #Crystal Ball Fit
	for i in range(h.GetNcells()):
		sh.SetBinContent(i,(h.GetBinError(i)))
	h3 = (h - h2)/sh # h = data, sh = sqrt(data)
	h3.SetTitle("")
	h3.GetXaxis().SetTitleSize(0.15)
	h3.GetXaxis().SetLabelSize(0.10)
	h3.GetXaxis().SetTitleOffset(0.84)
	h3.GetYaxis().SetTitleSize(0.1925)
	h3.GetYaxis().SetLabelSize(0.08)
	h3.GetYaxis().SetTitleOffset(0.84)
	h3.GetYaxis().SetNdivisions(10)
	#h3.SetTitle("Pull Plot (dR) [X300A75]")
	#h3.Draw("E")
	return h3