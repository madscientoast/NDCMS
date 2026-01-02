import ROOT
import sys

subname = str(sys.argv[1])
endp = float(sys.argv[2])

ms = ROOT.RooMsgService.instance()
ms.setGlobalKillBelow(ROOT.RooFit.FATAL)

# Load Data and Signal
f = ROOT.TFile("shapes_"+subname+".root", "READ") # I exported the data and original MC to this file. 

# Create a RooFit workspace and variables
w = ROOT.RooWorkspace("w")

# Define observable (x-axis of the histogram)
mass = ROOT.RooRealVar("mass", "mass", 150, endp)
weight = ROOT.RooRealVar("weights","weights",0,0,1)

##############################################################################################################################################################
#Make datahists for signal
signal_X500 = f.Get("signal_m500")
signal_hist_X500 = ROOT.RooDataSet(
    "X500_bin1", "X500_bin1",
    signal_X500,
    ROOT.RooArgSet(mass,weight),
     "", 
    "weights"
)

# Define parameters for the double-sided Crystal Ball function (signal)
mean_X500 = ROOT.RooRealVar("mean_X500_bin1", "mean_X500_bin1", 500, 480, 520)
sigma_X500 = ROOT.RooRealVar("sigma_X500_bin1", "sigma_X500_bin1", 10, 1, 15)
alpha1_X500 = ROOT.RooRealVar("alpha1_X500_bin1", "alpha1_X500_bin1", 1.5, 0.1, 5)
n1_X500 = ROOT.RooRealVar("n1_X500_bin1", "n1_X500_bin1", 2.0, 0.1, 5)
alpha2_X500 = ROOT.RooRealVar("alpha2_X500_bin1", "alpha2_X500_bin1", 1.5, 0.1, 5)
n2_X500 = ROOT.RooRealVar("n2_X500_bin1", "n2_X500_bin1", 2.0, 0.1, 5)

# Create the double-sided Crystal Ball PDF
cb_pdf_X500 = ROOT.RooDoubleCrystalBall("model_X500signal_bin1", "model_signalX500_bin1", mass, mean_X500, sigma_X500, alpha1_X500, n1_X500, alpha2_X500, n2_X500)

# Set parameters based on DCB fit
cb_pdf_X500.fitTo(signal_hist_X500,ROOT.RooFit.SumW2Error(True), ROOT.RooFit.PrintLevel(-1), ROOT.RooFit.Verbose(False))

# Set Signal params constant
mean_X500.setConstant(True)
sigma_X500.setConstant(True)
alpha1_X500.setConstant(True)
n1_X500.setConstant(True)
alpha2_X500.setConstant(True)
n2_X500.setConstant(True)
##############################################################################################################################################################
#Make datahists for signal
signal_X750 = f.Get("signal_m750")
signal_hist_X750 = ROOT.RooDataSet(
    "X750_bin1", "X750_bin1",
    signal_X750,
    ROOT.RooArgSet(mass,weight),
     "", 
    "weights"
)

# Define parameters for the double-sided Crystal Ball function (signal)
mean_X750 = ROOT.RooRealVar("mean_X750_bin1", "mean_X750_bin1", 750, 730, 770)
sigma_X750 = ROOT.RooRealVar("sigma_X750_bin1", "sigma_X750_bin1", 10, 1, 15)
alpha1_X750 = ROOT.RooRealVar("alpha1_X750_bin1", "alpha1_X750_bin1", 1.5, 0.1, 5)
n1_X750 = ROOT.RooRealVar("n1_X750_bin1", "n1_X750_bin1", 2.0, 0.1, 5)
alpha2_X750 = ROOT.RooRealVar("alpha2_X750_bin1", "alpha2_X750_bin1", 1.5, 0.1, 5)
n2_X750 = ROOT.RooRealVar("n2_X750_bin1", "n2_X750_bin1", 2.0, 0.1, 5)

# Create the double-sided Crystal Ball PDF
cb_pdf_X750 = ROOT.RooDoubleCrystalBall("model_X750signal_bin1", "model_signalX750_bin1", mass, mean_X750, sigma_X750, alpha1_X750, n1_X750, alpha2_X750, n2_X750)

# Set parameters based on DCB fit
cb_pdf_X750.fitTo(signal_hist_X750,ROOT.RooFit.SumW2Error(True), ROOT.RooFit.PrintLevel(-1), ROOT.RooFit.Verbose(False))

# Set Signal params constant
mean_X750.setConstant(True)
sigma_X750.setConstant(True)
alpha1_X750.setConstant(True)
n1_X750.setConstant(True)
alpha2_X750.setConstant(True)
n2_X750.setConstant(True)
##############################################################################################################################################################
#Make datahists for signal
signal_X1000 = f.Get("signal_m1000")
signal_hist_X1000 = ROOT.RooDataSet(
    "X1000_bin1", "X1000_bin1",
    signal_X1000,
    ROOT.RooArgSet(mass,weight),
     "", 
    "weights"
)

# Define parameters for the double-sided Crystal Ball function (signal)
mean_X1000 = ROOT.RooRealVar("mean_X1000_bin1", "mean_X1000_bin1", 1000, 800, 1200)
sigma_X1000 = ROOT.RooRealVar("sigma_X1000_bin1", "sigma_X1000_bin1", 100, 10, 200)
alpha1_X1000 = ROOT.RooRealVar("alpha1_X1000_bin1", "alpha1_X1000_bin1", 1.5, 0.1, 10)
n1_X1000 = ROOT.RooRealVar("n1_X1000_bin1", "n1_X1000_bin1", 2.0, 0.1, 30)
alpha2_X1000 = ROOT.RooRealVar("alpha2_X1000_bin1", "alpha2_X1000_bin1", 1.5, 0.1, 10)
n2_X1000 = ROOT.RooRealVar("n2_X1000_bin1", "n2_X1000_bin1", 2.0, 0.1, 30)

# Create the double-sided Crystal Ball PDF
cb_pdf_X1000 = ROOT.RooDoubleCrystalBall("model_X1000signal_bin1", "model_signalX1000_bin1", mass, mean_X1000, sigma_X1000, alpha1_X1000, n1_X1000, alpha2_X1000, n2_X1000)

# Set parameters based on DCB fit
cb_pdf_X1000.fitTo(signal_hist_X1000,ROOT.RooFit.SumW2Error(True), ROOT.RooFit.PrintLevel(-1), ROOT.RooFit.Verbose(False))

# Set Signal params constant
mean_X1000.setConstant(True)
sigma_X1000.setConstant(True)
alpha1_X1000.setConstant(True)
n1_X1000.setConstant(True)
alpha2_X1000.setConstant(True)
n2_X1000.setConstant(True)
##############################################################################################################################################################
#Make datahists for signal
signal_X1500 = f.Get("signal_m1500")
signal_hist_X1500 = ROOT.RooDataSet(
    "X1500_bin1", "X1500_bin1",
    signal_X1500,
    ROOT.RooArgSet(mass,weight),
     "", 
    "weights"
)

# Define parameters for the double-sided Crystal Ball function (signal)
mean_X1500 = ROOT.RooRealVar("mean_X1500_bin1", "mean_X1500_bin1", 1500, 1300, 1750)
sigma_X1500 = ROOT.RooRealVar("sigma_X1500_bin1", "sigma_X1500_bin1", 100, 10, 200)
alpha1_X1500 = ROOT.RooRealVar("alpha1_X1500_bin1", "alpha1_X1500_bin1", 1.5, 0.1, 10)
n1_X1500 = ROOT.RooRealVar("n1_X1500_bin1", "n1_X1500_bin1", 2.0, 0.1, 30)
alpha2_X1500 = ROOT.RooRealVar("alpha2_X1500_bin1", "alpha2_X1500_bin1", 1.5, 0.1, 10)
n2_X1500 = ROOT.RooRealVar("n2_X1500_bin1", "n2_X1500_bin1", 2.0, 0.1, 30)

# Create the double-sided Crystal Ball PDF
cb_pdf_X1500 = ROOT.RooDoubleCrystalBall("model_X1500signal_bin1", "model_signalX1500_bin1", mass, mean_X1500, sigma_X1500, alpha1_X1500, n1_X1500, alpha2_X1500, n2_X1500)

# Set parameters based on DCB fit
cb_pdf_X1500.fitTo(signal_hist_X1500,ROOT.RooFit.SumW2Error(True), ROOT.RooFit.PrintLevel(-1), ROOT.RooFit.Verbose(False))

# Set Signal params constant
mean_X1500.setConstant(True)
sigma_X1500.setConstant(True)
alpha1_X1500.setConstant(True)
n1_X1500.setConstant(True)
alpha2_X1500.setConstant(True)
n2_X1500.setConstant(True)
##############################################################################################################################################################
#Make datahists for signal
signal_X2000 = f.Get("signal_m2000")
signal_hist_X2000 = ROOT.RooDataSet(
    "X2000_bin1", "X2000_bin1",
    signal_X2000,
    ROOT.RooArgSet(mass,weight),
     "", 
    "weights"
)

# Define parameters for the double-sided Crystal Ball function (signal)
mean_X2000 = ROOT.RooRealVar("mean_X2000_bin1", "mean_X2000_bin1", 2000, 1800, 2200)
sigma_X2000 = ROOT.RooRealVar("sigma_X2000_bin1", "sigma_X2000_bin1", 100, 10, 200)
alpha1_X2000 = ROOT.RooRealVar("alpha1_X2000_bin1", "alpha1_X2000_bin1", 1.5, 0.1, 10)
n1_X2000 = ROOT.RooRealVar("n1_X2000_bin1", "n1_X2000_bin1", 2.0, 0.1, 30)
alpha2_X2000 = ROOT.RooRealVar("alpha2_X2000_bin1", "alpha2_X2000_bin1", 1.5, 0.1, 10)
n2_X2000 = ROOT.RooRealVar("n2_X2000_bin1", "n2_X2000_bin1", 2.0, 0.1, 30)

# Create the double-sided Crystal Ball PDF
cb_pdf_X2000 = ROOT.RooDoubleCrystalBall("model_X2000signal_bin1", "model_signalX2000_bin1", mass, mean_X2000, sigma_X2000, alpha1_X2000, n1_X2000, alpha2_X2000, n2_X2000)

# Set parameters based on DCB fit
cb_pdf_X2000.fitTo(signal_hist_X2000,ROOT.RooFit.SumW2Error(True), ROOT.RooFit.PrintLevel(-1), ROOT.RooFit.Verbose(False))

# Set Signal params constant
mean_X2000.setConstant(True)
sigma_X2000.setConstant(True)
alpha1_X2000.setConstant(True)
n1_X2000.setConstant(True)
alpha2_X2000.setConstant(True)
n2_X2000.setConstant(True)
##############################################################################################################################################################
#Make datahists for signal
signal_X3000 = f.Get("signal_m3000")
signal_hist_X3000 = ROOT.RooDataSet(
    "X3000_bin1", "X3000_bin1",
    signal_X3000,
    ROOT.RooArgSet(mass,weight),
     "", 
    "weights"
)

# Define parameters for the double-sided Crystal Ball function (signal)
mean_X3000 = ROOT.RooRealVar("mean_X3000_bin1", "mean_X3000_bin1", 3000, 2800, 3200)
sigma_X3000 = ROOT.RooRealVar("sigma_X3000_bin1", "sigma_X3000_bin1", 100, 10, 200)
alpha1_X3000 = ROOT.RooRealVar("alpha1_X3000_bin1", "alpha1_X3000_bin1", 1.5, 0.1, 10)
n1_X3000 = ROOT.RooRealVar("n1_X3000_bin1", "n1_X3000_bin1", 2.0, 0.1, 30)
alpha2_X3000 = ROOT.RooRealVar("alpha2_X3000_bin1", "alpha2_X3000_bin1", 1.5, 0.1, 10)
n2_X3000 = ROOT.RooRealVar("n2_X3000_bin1", "n2_X3000_bin1", 2.0, 0.1, 30)

# Create the double-sided Crystal Ball PDF
cb_pdf_X3000 = ROOT.RooDoubleCrystalBall("model_X3000signal_bin1", "model_signalX3000_bin1", mass, mean_X3000, sigma_X3000, alpha1_X3000, n1_X3000, alpha2_X3000, n2_X3000)

# Set parameters based on DCB fit
cb_pdf_X3000.fitTo(signal_hist_X3000,ROOT.RooFit.SumW2Error(True), ROOT.RooFit.PrintLevel(-1), ROOT.RooFit.Verbose(False))

# Set Signal params constant
mean_X3000.setConstant(True)
sigma_X3000.setConstant(True)
alpha1_X3000.setConstant(True)
n1_X3000.setConstant(True)
alpha2_X3000.setConstant(True)
n2_X3000.setConstant(True)

# Import to Workspace #
getattr(w, "import")(cb_pdf_X500)
getattr(w, "import")(cb_pdf_X750)
getattr(w, "import")(cb_pdf_X1000)
getattr(w, "import")(cb_pdf_X1500)
getattr(w, "import")(cb_pdf_X2000)
getattr(w, "import")(cb_pdf_X3000)

# Save workspace
w.writeToFile("signals_"+subname+"_workspace.root")
