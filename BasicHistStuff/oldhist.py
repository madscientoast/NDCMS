from ROOT import TFile, TH1D, TCanvas, TLegend

c1 = TCanvas()

f1 = TFile.Open("X300A15/7F4DE753-B11F-B445-A7FE-C0E7728CE935.root")
f2 = TFile.Open("X300A30/1958F18B-5F1E-054D-B649-49E015A38B33.root")
f3 = TFile.Open("X300A75/D1482C1E-00B7-444C-BE95-C9A289A80D7E.root")




e1 = f1.Events
e2 = f2.Events
e3 = f3.Events


h1 = TH1D("h1", "nPhoton [X300]", 100, 0.0, 100.0)
h2 = TH1D("h2", "h2", 100, 0.0, 100.0)
h3 = TH1D("h3", "h3", 100, 0.0, 100.0)


e1.Draw("nPhoton >> h1")
e2.Draw("nPhoton >> h2")
e3.Draw("nPhoton >> h3")

x = h1.GetXaxis()
y = h1.GetYaxis()
x.SetRange(0, 10)
x.SetTitle("nPhoton")
y.SetTitle("Events")

h1.SetLineColor(1)
h2.SetLineColor(2)
h3.SetLineColor(3)

h1.Scale(1./h1.Integral())
h2.Scale(1./h2.Integral())
h3.Scale(1./h3.Integral())
h1.SetMaximum(1.0)
h1.Draw("hist")
h2.Draw("hist SAME")
c1.Update()
h3.Draw("hist SAME")
c1.Update()

legend = TLegend(0.7, 0.35, 0.90, 0.57)
legend.AddEntry(h1, "#alpha = 0.05", "l")
legend.AddEntry(h2, "#alpha = 0.1", "l")
legend.AddEntry(h3, "#alpha = 0.25", "l")
legend.SetBorderSize(0)
legend.Draw()
c1.SetTitle("nPhoton")
h1.SetStats(0)

c1.Update()
c1.SaveAs("nPhoton_X300.pdf")
#input("Press Enter to exit...")