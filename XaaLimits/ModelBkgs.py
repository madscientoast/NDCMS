import ROOT
import sys

endp = float(sys.argv[1])

ms = ROOT.RooMsgService.instance()
ms.setGlobalKillBelow(ROOT.RooFit.FATAL)

# Load Data and Signal
f = ROOT.TFile("bkgA_2018.root", "READ") # I exported the data and original MC to this file. 
data = f.Get("data_obs")

# Define observable (x-axis of the histogram)
mass = ROOT.RooRealVar("mass", "mass", 150,endp)
weight = ROOT.RooRealVar("weights","weights",0,0,1)


#Make dataset for data
data_hist = ROOT.RooDataSet(
    "data_obs", "data_obs",
    data,
    ROOT.RooArgSet(mass,weight),
     "", 
    "weights"
)
print(data_hist.sumEntries())

# Define Parameters for Background Fits
# ATLAS 
atl0 = ROOT.RooRealVar("atl0", "Norm", 0.01, 1e-6, 10)   
atl1 = ROOT.RooRealVar("atl1", "Power Term", 5.0, 1e-6, 10)
atl2 = ROOT.RooRealVar("atl2", "Exponential Term", 0.02, 1e-6, 10)

# ModDijet
dij0 = ROOT.RooRealVar("dij0", "Norm", 1.0, 1e-4, 100)   
dij1 = ROOT.RooRealVar("dij1", "Power Term 1", -1.0, -10, -1)
dij2 = ROOT.RooRealVar("dij2", "Power Term 2", 4.0, 1, 10)

# Diphoton
dip0 = ROOT.RooRealVar("dip0", "Norm", 1e-02, 1e-4, 10)   
dip1 = ROOT.RooRealVar("dip1", "Exponent Base", 5.0, -10, 10)
dip2 = ROOT.RooRealVar("dip2", "Logarithmic Term", -1.0, -10, 10)

# Power
pwr0 = ROOT.RooRealVar("pwr0", "Norm", 1.00000e-02, 1e-6, 10)   
pwr1 = ROOT.RooRealVar("pwr1", "Exponent Base", 5.98255e+00, 1e-6, 10)
pwr2 = ROOT.RooRealVar("pwr2", "Logarithmic Term", 0.1, 1e-6, 10)
pwr3 = ROOT.RooRealVar("pwr3", "Other Term", 400, 300, 800)



# Create the Background PDFs
# ATLAS Background
model_atlas_bkg = ROOT.RooGenericPdf(
    "model_atlas_bkg_bin1", "(atl0 / pow(mass, atl1)) * exp(-atl2 * mass)", ROOT.RooArgList(mass, atl0, atl1, atl2)
)

# ModDijet
model_dijet_bkg = ROOT.RooGenericPdf(
    "model_dijet_bkg_bin1", "dij0 * (pow(1, dij1) - pow(mass,dij1/3))/pow(mass,dij2)", ROOT.RooArgList(mass, dij0, dij1, dij2)
)

# Diphoton Background
model_diphoton_bkg = ROOT.RooGenericPdf(
    "model_diphoton_bkg_bin1", "dip0 * pow(mass, (dip1 + dip2 * log(mass)))", ROOT.RooArgList(mass, dip0, dip1, dip2)
)

# Power Law Background
model_power_bkg = ROOT.RooGenericPdf(
    "model_power_bkg_bin1", "pwr0 * pow(pwr1, pwr2 * mass) * pow(pwr1, pwr3/mass)", ROOT.RooArgList(mass, pwr0, pwr1, pwr2, pwr3)
)

# Performt he fits
model_atlas_bkg.fitTo(data_hist, ROOT.RooFit.Minimizer("Minuit2","minimize"), ROOT.RooFit.SumW2Error(True), ROOT.RooFit.PrintLevel(-1), ROOT.RooFit.Verbose(False))
model_dijet_bkg.fitTo(data_hist, ROOT.RooFit.Minimizer("Minuit2","minimize"), ROOT.RooFit.SumW2Error(True), ROOT.RooFit.PrintLevel(-1), ROOT.RooFit.Verbose(False))
model_diphoton_bkg.fitTo(data_hist, ROOT.RooFit.Minimizer("Minuit2","minimize"), ROOT.RooFit.SumW2Error(True), ROOT.RooFit.PrintLevel(-1), ROOT.RooFit.Verbose(False))
model_power_bkg.fitTo(data_hist, ROOT.RooFit.Minimizer("Minuit2","minimize"), ROOT.RooFit.SumW2Error(True), ROOT.RooFit.PrintLevel(-1), ROOT.RooFit.Verbose(False))

cat = ROOT.RooCategory("pdfindex_bin1", "Index of Pdf which is active for bin1")

models = ROOT.RooArgList()
models.add(model_atlas_bkg)
models.add(model_dijet_bkg)
models.add(model_diphoton_bkg)
models.add(model_power_bkg)

# Make MultiPDF for all models 
multipdf = ROOT.RooMultiPdf("multipdf_bin1", "MultiPdf for bin1", cat, models)

# Define norm
norm = ROOT.RooRealVar("multipdf_bin1_norm", "Number of background events in bin1", data_hist.sumEntries(), 0, 3*data_hist.sumEntries())

# Make output #
f_out = ROOT.TFile("workspace_bkgALL.root", "RECREATE")
w = ROOT.RooWorkspace("w")

# Import to Workspace #
getattr(w, "import")(data_hist)
getattr(w, "import")(cat)
getattr(w, "import")(norm)
getattr(w, "import")(multipdf)

# Save workspace
w.Write()
f_out.Close()
