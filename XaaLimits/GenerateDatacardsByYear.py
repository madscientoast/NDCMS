# Make Datacards for more pure regime #
def MakeDatacard(signal,dir,b):
    fname = dir+"/datacard_m"+signal+".txt"
    with open(fname,"w") as file:
        file.write("""imax 1
jmax 1
kmax *
---------------------------------------------
""")
        # Signal Models #
        line = "shapes signal_model    bin2016    signals_"+dir+"2016_workspace.root    w:model_"+signal+"signal_bin2016\n"
        file.write(line)
        line = "shapes signal_model    bin2017    signals_"+dir+"2017_workspace.root    w:model_"+signal+"signal_bin2017\n"
        file.write(line)
        line = "shapes signal_model    bin2018    signals_"+dir+"2018_workspace.root    w:model_"+signal+"signal_bin2018\n"
        file.write(line)

        # Background Models #
        line = "shapes bkg_model       bin2016    workspace_bkg"+b+"_2016.root           w:multipdf_bin2016\n"
        file.write(line)
        line = "shapes bkg_model       bin2017    workspace_bkg"+b+"_2017.root           w:multipdf_bin2017\n"
        file.write(line)
        line = "shapes bkg_model       bin2018    workspace_bkg"+b+"_2018.root           w:multipdf_bin2018\n"
        file.write(line)

        # Data #
        line = "shapes data_obs        bin2016    workspace_bkg"+b+"_2016.root           w:data_obs"
        file.write(line)
        line = "shapes data_obs        bin2017    workspace_bkg"+b+"_2017.root           w:data_obs"
        file.write(line)
        line = "shapes data_obs        bin2018    workspace_bkg"+b+"_2018.root           w:data_obs"
        file.write(line)
        file.write("""
---------------------------------------------
bin         bin2016     bin2017     bin2018
observation -1          -1          -1
---------------------------------------------
bin         bin2016       bin2016       bin2017         bin2017     bin2018         bin2018
process     signal_model  bkg_model     signal_model    bkg_model   signal_model    bkg_model
process     0             1             0               1           0               1
rate        1.0           1.0           1.0             1.0         1.0             1.0
---------------------------------------------
lumi        lnN           1.025        -    1.025   -   1.025   -
CMS_hgg_phoIdMva      lnN      1.005    -   1.005   -   1.005   - 
CMS_pileup            lnN      0.977/1.023      -   0.977/1.023     -   0.977/1.023     -
---------------------------------------------
pdfindex_bin2016         discrete
pdfindex_bin2017         discrete
pdfindex_bin2018         discrete
""")
        
# Make Datacards for combined regime #
def MakeDatacard2(signal,dir,b):
    fname = dir+"/datacard_m"+signal+b+".txt"
    with open(fname,"w") as file:
        file.write("""imax 1
jmax 1
kmax *
---------------------------------------------
""")
        # Signal Models #
        line = "shapes signal_model    bin2016    signals_"+dir+"2016_workspace.root    w:model_"+signal+"signal_bin2016\n"
        file.write(line)
        line = "shapes signal_model    bin2017    signals_"+dir+"2017_workspace.root    w:model_"+signal+"signal_bin2017\n"
        file.write(line)
        line = "shapes signal_model    bin2018    signals_"+dir+"2018_workspace.root    w:model_"+signal+"signal_bin2018\n"
        file.write(line)

        # Background Models #
        line = "shapes bkg_model       bin2016    workspace_bkg"+b+"_2016.root           w:multipdf_bin2016\n"
        file.write(line)
        line = "shapes bkg_model       bin2017    workspace_bkg"+b+"_2017.root           w:multipdf_bin2017\n"
        file.write(line)
        line = "shapes bkg_model       bin2018    workspace_bkg"+b+"_2018.root           w:multipdf_bin2018\n"
        file.write(line)

        # Data #
        line = "shapes data_obs        bin2016    workspace_bkg"+b+"_2016.root           w:data_obs"
        file.write(line)
        line = "shapes data_obs        bin2017    workspace_bkg"+b+"_2017.root           w:data_obs"
        file.write(line)
        line = "shapes data_obs        bin2018    workspace_bkg"+b+"_2018.root           w:data_obs"
        file.write(line)
        file.write("""
---------------------------------------------
bin         bin2016     bin2017     bin2018
observation -1          -1          -1
---------------------------------------------
bin         bin2016       bin2016       bin2017         bin2017     bin2018         bin2018
process     signal_model  bkg_model     signal_model    bkg_model   signal_model    bkg_model
process     0             1             0               1           0               1
rate        1.0           1.0           1.0             1.0         1.0             1.0
---------------------------------------------
lumi        lnN           1.025        -    1.025   -   1.025   -
CMS_hgg_phoIdMva      lnN      1.005    -   1.005   -   1.005   - 
CMS_pileup            lnN      0.977/1.023      -   0.977/1.023     -   0.977/1.023     -
---------------------------------------------
""")
        line = "pdfindex_bin2016"+b+ "      discrete\n"
        file.write(line)
        line = "pdfindex_bin2017"+b+ "      discrete\n"
        file.write(line)
        line = "pdfindex_bin2018"+b+ "      discrete\n"
        file.write(line)

mrange = ["X500","X750","X1000","X1500","X2000","X3000"]

for m in mrange:
    MakeDatacard(m,"0p05","A")
    MakeDatacard2(m,"0p1","A")
    MakeDatacard2(m,"0p1","B")
    MakeDatacard2(m,"0p25","A")
    MakeDatacard2(m,"0p25","B")
    MakeDatacard(m,"0p4","B")



