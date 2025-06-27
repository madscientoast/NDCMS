import ROOT
from ROOT import *
from array import array
import os

def AddCMSLumi(pad, fb, extra):
	cmsText     = "CMS " + extra
	cmsTextFont   = 61  
	lumiTextSize     = 0.45
	lumiTextOffset   = 0.15
	cmsTextSize      = 0.5
	cmsTextOffset    = 0.15
	H = pad.GetWh()
	W = pad.GetWw()
	l = pad.GetLeftMargin()
	t = pad.GetTopMargin()
	r = pad.GetRightMargin()
	b = pad.GetBottomMargin()
	e = 0.025
	pad.cd()
	lumiText = str(fb)+" fb^{-1} (13 TeV)"
	latex = TLatex()
	latex.SetNDC()
	latex.SetTextAngle(0)
	latex.SetTextColor(kBlack)	
	extraTextSize = 0.76*cmsTextSize
	latex.SetTextFont(42)
	latex.SetTextAlign(31) 
	latex.SetTextSize(lumiTextSize*t)	
	latex.DrawLatex(1-r,1-t+lumiTextOffset*t,lumiText)
	pad.cd()
	latex.SetTextFont(cmsTextFont)
	latex.SetTextSize(cmsTextSize*t)
	latex.SetTextAlign(11)
	latex.DrawLatex(0.1265, 0.825, cmsText)
	pad.Update()

# Open the TMVA output and background file
tmva_file = ROOT.TFile("TMVA_BDT_output_ALL.root")
background_file = ROOT.TFile("bkg.root")
background_tree = background_file.Get("Events")

# Load the trained BDT
reader = ROOT.TMVA.Reader()

# Define variables (these must match the training setup)
m_asym = array('f', [0])
deltaEta = array('f', [0])
dR1 = array('f', [0])
dR2 = array('f', [0])

reader.AddVariable("m_asym", m_asym)
reader.AddVariable("deltaEta", deltaEta)
reader.AddVariable("dR1", dR1)
reader.AddVariable("dR2", dR2)

# Load the BDT weights
reader.BookMVA("BDT", "dataset/weights/TMVAClassification_BDT.weights.xml")

# Find the optimal BDT score threshold from the ROC curve
roc_curve = tmva_file.Get("dataset/Method_BDT/BDT/MVA_BDT_rejBvsS")
best_bdt_score = 0.2 # Setting a control region basically


print(f"Optimal BDT score threshold: {best_bdt_score:.3f}")

# Histogram for the background `m_Xm` distribution after the BDT cut
hist_bkg_Xm = ROOT.TH1F("bkg_m_Xm", "Background m_Xm After BDT Cut; m_Xm; Events", 200, 0, 1000)

# Fill the histogram with `m_Xm` from the background tree
for event in background_tree:
    m_asym[0] = event.m_asym
    deltaEta[0] = event.deltaEta
    dR1[0] = event.dR1
    dR2[0] = event.dR2
    bdt_score = reader.EvaluateMVA("BDT")
    if bdt_score > best_bdt_score:  # Apply the BDT cut
        hist_bkg_Xm.Fill(event.m_Xm)

# Draw the histogram
canvas = ROOT.TCanvas("c1", "Background m_Xm Distribution", 800, 600)
hist_bkg_Xm.SetTitle("4-mass After BDT Cut; 4-mass (GeV); Events")
hist_bkg_Xm.Draw("E0")


# Ensure output directory exists
output_dir = "03-05-2025"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

obs_out = TFile(f"{output_dir}/obs_out.root", "RECREATE")

if not obs_out or obs_out.IsZombie():
    print("Error: Failed to open ROOT file for writing.")
    exit(1)

# Check if histogram is valid
if hist_bkg_Xm is None:
    print("Error: h_extended is None before writing!")
    exit(1)

# Ensure histogram stays in memory
hist_bkg_Xm.SetDirectory(0)
hist_bkg_Xm.Write("data_obs")


# Close file
obs_out.Close()
print("File successfully written!")

AddCMSLumi(canvas, 1.1, "Preliminary")
# Save the histogram as an image
canvas.SaveAs("Background_m_Xm_Distribution.root")

print("Background m_Xm distribution saved as 'Background_m_Xm_Distribution.root'.")
