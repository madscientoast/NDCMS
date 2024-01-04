from ROOT import TFile, TH1D, TCanvas, TLorentzVector



c1 = TCanvas()
f1 = TFile.Open("X300A15/7F4DE753-B11F-B445-A7FE-C0E7728CE935.root")
e1 = f1.Events
v_arr = []

pt = e1.GetLeaf("Photon_pt").GetValue(800)
phi = e1.GetLeaf("Photon_phi").GetValue(800)
eta = e1.GetLeaf("Photon_eta").GetValue(800)
m = e1.GetLeaf("Photon_mass").GetValue(800)
v = TLorentzVector(pt,eta,phi,m)

pt = e1.GetLeaf("Photon_pt").GetValue(801)
phi = e1.GetLeaf("Photon_phi").GetValue(801)
eta = e1.GetLeaf("Photon_eta").GetValue(801)
m = e1.GetLeaf("Photon_mass").GetValue(801)
y = TLorentzVector(pt,eta,phi,m)

dR = y.DeltaR(v)    #Seem to have proven that I kinda know how to do this?
print(dR)
'''
for e in e1:
    pt = e.GetLeaf("Photon_pt").GetValue()
    phi = e.GetLeaf("Photon_phi").GetValue()
    eta = e.GetLeaf("Photon_eta").GetValue()
    m = e.GetLeaf("Photon_mass").GetValue()
    v = TLorentzVector(pt,eta,phi,m)
    print(v.pt())
    v_arr.append(v)
'''


print("done")

'''h1 = TH1D("h1", "Photon #phi [X300A15]", 100, 0.0, 100.0)
e1.Draw("Photon_phi >> h1")
h1.Draw("hist")

h1.SetStats(0)
x = h1.GetXaxis()
y = h1.GetYaxis()
x.SetRange(-4,4)
x.SetLimits(-4,4)
x.SetTitle("#phi")
y.SetTitle("Events")
c1.Update()
c1.SaveAs("test.pdf")'''