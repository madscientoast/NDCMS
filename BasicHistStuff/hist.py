import easyhist as easy

c1 = easy.TCanvas()
d = "X3000A750/"
var = "nPhoton"

a = easy.SetupFiles(d)
files = easy.LoadFiles(d, a)
events = [f.Events for f in files]

hs = var + " " + d[:-1]
h = easy.CreateHist(events,hs)
easy.Draw(events,h,var)
easy.Render(h,c1)
c1.SaveAs("X3000A750/nPhoton.pdf")