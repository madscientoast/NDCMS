import ROOT
from ROOT import *
from array import array
import os

# Define Signals #
signals = ["signal15.root","signal30.root","signal75.root"]
names = ["signal_m15","signal_m30","signal_m75"]

# Ensure output directory exists
output_dir = "ChooseBinning/10/"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

signals_out = TFile(f"{output_dir}/signals_out.root", "RECREATE")

if not signals_out or signals_out.IsZombie():
    print("Error: Failed to open ROOT file for writing.")
    exit(1)

for i in range(len(signals)):
    background_file = ROOT.TFile(signals[i], "READ")
    background_tree = background_file.Get("Events")
    
	# Histogram for the background `m_Xm` distribution after the BDT cut
    hist_bkg_Xm = ROOT.TH1F("bkg_m_Xm", "Background m_Xm After BDT Cut; m_Xm; Events", 100, 0, 1000)

	# Fill the histogram with `m_Xm` from the background tree
    for event in background_tree:
         hist_bkg_Xm.Fill(event.m_Xm)

	# Draw the histogram
    canvas = ROOT.TCanvas("c1", "Background m_Xm Distribution", 800, 600)
    hist_bkg_Xm.SetTitle("4-mass After BDT Cut; 4-mass (GeV); Events")
    hist_bkg_Xm.Draw("E0")

	# Check if histogram is valid
    if hist_bkg_Xm is None:
          print("Error: h_extended is None before writing!")
          exit(1)

	# Ensure histogram stays in memory
    hist_bkg_Xm.SetDirectory(0)
    # Set the output file as active before writing
    signals_out.cd()
    hist_bkg_Xm.Write(names[i])


# Close file
signals_out.Close()
print("Files successfully written!")

