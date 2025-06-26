# Introduction

This guide exists to document the process of signal generation for XaaTo4G analyses. It is loosely based on the old guide produced by Stephen. I basically ported this from my gDoc.
[Google Doc](https://docs.google.com/document/d/1FBYBmDTj9iCzCRH8slCoI9m6xzZz-AeQn_ow-OLxvKM/edit?usp=sharing)

![](https://opendata.cern.ch/static/docs/cms-mc-production-overview/diagram.png)

Signal generation is the combination of the steps described above. The intention of this document is to walk you through how to do each step. 

* GEN-SIM: For the initial generation we start in MadGraph with our model. We’ll get cards as output. We turn these cards into gridpacks which can be utilized throughout the rest of the simulation. After gridpacks are created we can run them through cmsDriver to complete the GEN-SIM step. The output will be a ROOT file, but it isn’t quite in a usable form yet.   
* DIGI-L1-DATAMIX-HLT(PREMIX): Here we will digitize our sample, add PU we will generate and triggers.  
* AODSIM,miniAOD,nanoAOD: Does the event reconstruction then reduces file size and brings the ROOT file to a more useful form.

This guide assumes that you have all necessary accounts required for signal generation (Compute, CERN/CMS VOMS, git, etc.)

# 1\. Install/Setup

## You’ll need a CMSSW environment first


  **General Way:** 
  ```csh 
  setenv VO_CMS_SW_DIR /cvmfs/cms.cern.ch 
  source $VO_CMS_SW_DIR/cmsset_default.csh 
  setenv SCRAM_ARCH slc6_amd64_gcc630 
  cmsrel CMSSW_10_1_0 
  cd CMSSW_10_1_0 
  cd src cmsenv 
  ``` 

**What’s need at time of writing this document on NDCRC:**
```csh
cmssw-el7
export SCRAM_ARCH=slc7_amd64_gcc10 	#required for requirred CMSSW
cmsrel CMSSW_12_2_3 #last release to support required HLT Menu
cd CMSSW_12_2_3/src/
cmsenv
```

After we get a CMSSW environment we will want to check out some additional tools/scripts. Namely, we want all the python files necessary for our cmsDriver/cmsRun commands. We also want genproductions for the scripts necessary to make gridpacks.

**For these we run:**
```csh
git cms-init
git cms-addpkg Configuration
git cms-addpkg HLTrigger/Configuration
git clone https://github.com/cms-sw/genproductions.git genproductions
```

Next, is the MadGraph specific setup. This is specified based on the model we are using, so one follows much from Stephen’s instructions here. 

Download and Install Madgraph. Stephen originally used MG v2.6.2, we will be using the most recent build at the time I started writing this guide. ([https://launchpad.net/mg5amcnlo/3.0/3.6.x/+download/MG5\_aMC\_v3.6.2.tar.gz](https://launchpad.net/mg5amcnlo/3.0/3.6.x/+download/MG5_aMC_v3.6.2.tar.gz))  
(If the link is broken just visit launchpad to find the build.)

**Proceed as follows:**
```csh
tar -zxvf MG5_aMC_v3.6.2.tar.gz   # can use curl or ssh upload to get MG on cluster
cd MG5_aMC_v3_6_2		         #go into MG directory
mkdir HEPTools 
```

Download LHAPDF and manually install it (DO NOT USE “install” INSIDE MG5). Stephen used LHAPDF v6.2.1, we will be using the newest version (v6.5.5) The link will follow below: [https://lhapdf.hepforge.org/downloads/?f=LHAPDF-6.5.5.tar.gz](https://lhapdf.hepforge.org/downloads/?f=LHAPDF-6.5.5.tar.gz)  
**Then, install as follows**
```csh
#(somewhere outside MG directory)
./configure --prefix=/path/to/MG5_aMC_v3_6_2/HEPTools/lhapdf6
make
make install
```
Then change: 
MG5_aMC_v2_6_2/input/mg5_configuration.txt:
\# lhapdf \= lhapdf-config (default, change this to next line:)
lhapdf = /path/to/MG5_aMC_v3_6_2/HEPTools/lhapdf6/bin/lhapdf-config #(change it to this!) 


Similarly to LHAPDF, Download (v 3.3.1) and Install FastJet. Stephen used v3.3.1. At the time of starting this guide I used v3.4.3 but you can get whatever version here: [https://fastjet.fr/](https://fastjet.fr/)  
**Follow as proceeds**
```csh
#(somewhere outside MG directory)
tar -zxvf fastjet-3.4.3.tar.gz
cd fastjet-3.4.3
./configure --prefix= /path/to/MG5_aMC_v3_6_2/HEPTools/fastjet/
make
make check
make install
```
Then change:  
MG5_aMC_v2_6_2/input/mg5_configuration.txt\:  	
\# fastjet = fastjet-config (default, change this to next line:)  	
fastjet =  /path/to/MG5_aMC_v3_6_2/HEPTools/fastjet (change it to this!)  

Then we can install the last couple MG tools within MG as Stephen did in his guide
```csh
#(cd in MG directory)
./bin/mg5_aMC
install pythia8
install ninja
```

Provided you have received the proper model files you can proceed with signal generation. This guide assumes you are using some variant of the Phi2\_simp\_tt model. Stephen’s guide referred to Phi2\_simp\_tt, but I am using *Phi2\_simp\_tt\_qed*. Phi2\_simp\_tt\_qed2 is an alternative that also exists according to CMSSW. 

Note: LHAPDF python interface is finicky about versioning. We can either rollback to match the CMSSW python or use the NDCRC modules, such as:

module load python/3.12.8

Addendum: If you are using singularities for older architectures (i.e. slc6/slc7) you will need to unset libraries or else you’ll get compatibility issues.

```csh
unset PERL5LIB
unset PYTHONPATH
unset LD_LIBRARY_PATH
```

# 2\. MadGraph Card Generation

Here we will proceed with MadGraph card and LHE file generation guided by Stephen’s old instructions. The output here will then be tuned to be acceptable by the gridpack generation script(s) from genproductions. 

**Begin by starting MG5 and loading our model**
```csh
cd /path/to/MG5_aMC_v3.6.2
./bin/mg5_aMC
import model Phi2_simp_tt_qed
generate p p > y0 [QCD] QED = 0 @0 
```

**Here, the process can diverge depending on MG5 versions. In older version we could add processes without NLO/LO issues, but newer versions of MG5 take issue with mixing NLO/LO so we must use \[noborn=QCD\].**

*Note: I validated whether there was any physics difference doing this, and there isn’t. It produces the same processes and diagrams as it did the old way in the version of MG5 Stephen used.*

```csh
add process p p > y0 j [noborn=QCD] QED = 0 @1
add process p p > y0 j j [noborn=QCD] QED = 0 @2
output XaaTEST_XYZ #name whatever you want 
```

**This gets you most of what’s required to start converting MG output to a gridpack, we can prefill more into the cards by continuing through Stephen’s instructions.** 
```csh
launch
madspin=ON
<enter>
set mass 6 10000
set mass 54 300 #Set your X Mass
set mass 90000054 20 #Set the phi mass
compute_widths 6
compute_widths 54
compute_widths 90000054
<enter>
```

### Along the way we are given a chance to edit the cards before we get our processes as output. We start by following Stephen’s instructions, but will later modify as required based off of gridpack requirements to compile and referring to the Card references the original configuration refers to. 

Stephen says continue as:  
*First, change me5\_configuration.txt to reflect the changes you made in mg5\_configuration.txt.*

*Then:*   
*(in run\_card.dat)*

* **Number of Events (Set near top of file, line 31 if no inserts)**
  ```csh
  100000 = nevents ! Number of unweighted events requested
  ```  
* **PDFS (PDF Choice block, line 44 if no inserts)**  
  ```csh
  nn23lo1    = pdlabel     ! PDF set  
  230000    = lhaid     ! if pdlabel=lhapdf, this is the lhapdf number
  ```

  becomes:

  ```csh
  lhapdf	= pdlabel ! PDF set  
  306000	= lhaid ! if pdlabel=lhapdf, this is the lhapdf number```  
* **Matching parameters (Matching parameter (MLM only), line 69 if no insterts)**  
  ```csh
  1 = ickkw            ! 0 no matching, 1 MLM  
  1.0 = alpsfact         ! scale factor for QCD emission vx  
  False = chcluster        ! cluster only according to channel diag  
  5 = asrwgtflavor     ! highest quark flavor for a_s reweight  
  False  = auto_ptj_mjj  ! Automatic setting of ptj and mjj if xqcut >0  
  ! (turn off for VBF and single top processes)  
  30.0   = xqcut   ! minimum kt jet measure between partons
  ```

  becomes:

  ```csh
  1	= ickkw \! 0 no matching, 1 MLM  
  1     = highestmult ! for ickkw=2, highest mult group  
  1     = ktscheme ! for ickkw=1, 1 Durham kT, 2 Pythia pTE  
  1.0	= alpsfact ! scale factor for QCD emission vx  
  False	= chcluster ! cluster only according to channel diag  
  False = pdfwgt ! for ickkw=1, perform pdf reweighting  
  5	= asrwgtflavor ! highest quark flavor for a_s reweight  
  True	= auto_ptj_mjj ! Automatic setting of ptj and mjj if xqcut >0  
                                     ! (turn off for VBF and single top processes)   
  100.0	= xqcut ! minimum kt jet measure between partons```  
* **Minimum jet pT (mins and max block, line 115 after above changes)**  
  ```csh
  20.0 → 0.0 for ptj value
  ```

We then can refer to the CMSSW reference for necessary adjustments as needed.   
[https://github.com/cms-sw/genproductions/tree/mg27x/bin/MadGraph5\_aMCatNLO/cards/production/2017/13TeV/XtoAAto4G/XtoAAto4G\_X500A5](https://github.com/cms-sw/genproductions/tree/mg27x/bin/MadGraph5_aMCatNLO/cards/production/2017/13TeV/XtoAAto4G/XtoAAto4G_X500A5)

More on editing these cards in the next section though. 

# 3\. Gridpack Production

Now that we’ve run MadGraph, we need to take our Cards and produce a gridpack. 

### The first thing to do is to copy your MG project cards to your gridpack generation path in genproductions (the gridpack script is finicky about the path). We will also need to rename the primary cards with our project name as a prefix. 

**Here’s an example of how to do this:**
```csh
cp -r  /path/to/XaaTo4G_X300A20/Cards /path/to/genproductions/bin/MadGraph5_aMCatNLO
cd /path/to/genproductions/bin/MadGraph5_aMCatNLO/Cards
mv proc_card_mg5.dat XaaTo4G_X300A20_proc_card.dat
mv run_card.dat XaaTo4G_X300A20_run_card.dat
mv param_card.dat XaaTo4G_X300A20_param_card.dat
mv madspin_card.dat XaaTo4G_X300A20_madspin_card.dat
```

### Next, we will make a customize card that enters parameters for the gridpack. We use Stephen’s old setup as a guide ([https://github.com/cms-sw/genproductions/tree/mg27x/bin/MadGraph5\_aMCatNLO/cards/production/2017/13TeV/XtoAAto4G/XtoAAto4G\_X500A5](https://github.com/cms-sw/genproductions/tree/mg27x/bin/MadGraph5_aMCatNLO/cards/production/2017/13TeV/XtoAAto4G/XtoAAto4G_X500A5)). The only differences here are that we choose our X, a masses and may have different decay widths. Refer to your proc\_card output for your decay widths (i.e. for PIDs 6, 54, and 90000054). PID 6 should always have the same mass and decay width. DM parameters stay the same as well.

```csh
nano XaaTo4G_X300A20_customizecards.dat
set param_card mass 54 3.000000e+02
set param_card decay 54 1.314449e-02
set param_card mass 90000054 2.000000e+01
set param_card decay 90000054 1.970744e+00
set param_card mass 6 1.000000e+04
set param_card decay 6 3.281569e+05
set param_card dminputs 1.000000e+00
set param_card dminputs 2 0.000000e+00
set param_card dminputs 3 1.000000e+00
set param_card dminputs 4 0.000000e+00
set param_card dminputs 5 1.000000e+00
set param_card dminputs 6 1.000000e+00
set param_card dminputs 7 0.000000e+00
set param_card dminputs 8 0.000000e+00
set param_card dminputs 9 1.000000e+01
set param_card dminputs 10 1.000000e+04
set param_card dminputs 11 1.000000e+00
set param_card dminputs 12 0.000000e+00
```

Exit out and save. 

### Next, we have to make some edits to the process card or this will crash on gridpack generation. 

These lines need to be commented out:

* set include\_lepton\_initiated\_processes False  
* set nlo\_mixed\_expansion True

Goes to:

* \#set include\_lepton\_initiated\_processes False  
* \#set nlo\_mixed\_expansion True

Now, in order to import the model we need to give the full path to it.  
Change this line:

* import model Phi2\_simp\_tt\_qed

To:

* import model /path/to/MG5\_aMC\_v3\_6\_2/models/Phi2\_simp\_tt\_qed

### Then, we have to make a couple edits to the run card, namely just commenting out these lines in particular:

*   \= custom\_fcts \! List of files containing user hook function  
* 0.0  \= dsqrt\_shat \! minimal shat for full process

After the required modifications to the MG Cards are made, and all packages downloaded we’re almost ready. Before we do that just make a tiny fix to the gridpack generation script, we want to comment out a little line that removes necessary files.  
Comment out this:

* ${helpers\_dir}/cleangridmore.sh

We will also have to make a slight edit to the CMSSW version that is packaged with the gridpack when we are in the slc7 singularity/container. 

Seek out the section that defines CMSSW\_VERSION.

```python
if [[ $SYSTEM_RELEASE == *"release 7"* ]]; then
    cmssw_version=CMSSW_12_4_8
```

Change the second line to the following.

* cmssw\_version=CMSSW\_12\_2\_3

You may also want to copy the line that copies MG to the gridpack after the cleanup again to ensure that it isn’t missing necessary files. 

You want to copy your cards to the genproductions directory as it doesn’t do well in pointing outside of it. 
**Then just do the following.** 
```csh
cp -r /path/to/XaaTEST/Cards/ /path/to/genproductions/bin/MadGraph5_aMCatNLO/
cd /path/to/genproductions/bin/MadGraph5_aMCatNLO
./gridpack_generation.sh OUTPUT_NAME CARDS_DIR/ local
```

Now that you have a gridpack, it can be used to do the GEN-SIM step in simulation. **Good here.**

*Note: We will eventually automate the process of making cards and required edits, this is just the instructions for learning how to make it work at all.*

*Note 2: If you run into Python versioning errors you may need to add explicit lines to fix python version and libs in the gridpack generation file as well as the the runcmsgrid\_LO and runcmsgrid\_NLO files (after the eval runtime line in each)*

# 4\. GEN-SIM

### Now that we have a gridpack, we can start the rest of the simulation process. By means of DAS or MCM one can track down the old simulation commands ([https://cms-pdmv-prod.web.cern.ch/mcm/requests?dataset\_name=XtoAAto4G\_X300A15\_TuneCP5\_13TeV-madgraph-pythia8\&page=0\&shown=127](https://cms-pdmv-prod.web.cern.ch/mcm/requests?dataset_name=XtoAAto4G_X300A15_TuneCP5_13TeV-madgraph-pythia8&page=0&shown=127))

### This chain starts at LHEGS (i.e. LHE \+ GEN-SIM), so click the second button and you’ll see what commands are required. Inside you’ll see a curl command which will point you to where the original code fragment required to run this with cmsDriver/cmsRun. Grab that and change just the gridpack tarball it refers to, to your own. 

args \= cms.vstring('/path/to/genproductions/bin/MadGraph5\_aMCatNLO/XaaTo4G\_X300A20\_el9\_amd64\_gcc11\_CMSSW\_13\_2\_9\_tarball.tar.xz')

### Alternatively, you can also grab a version of the file off of my github. 

[(https://github.com/madscientoast/NDCMS/blob/master/Simulation/XaaTo4G.py)](https://github.com/madscientoast/NDCMS/blob/master/Simulation/XaaTo4G.py)

**From the same reference we will then run mostly the same cmsDriver command, but slightly modified so that it doesn’t spit errors at us** 
```csh
export SEED=$(($(date +%s) % 100 + 1))
cmsDriver.py Configuration/Generator/python/your_fragment.py \
--eventcontent RAWSIM,LHE \
--customise Configuration/DataProcessing/Utils.addMonitoring \
--datatier GEN-SIM,LHE --conditions auto:phase1_2018_realistic \
--beamspot Realistic25ns13TeVEarly2018Collision \
--customise_commands process.RandomNumberGeneratorService.externalLHEProducer.initialSeed="int(${SEED})" \
--step LHE,GEN,SIM --geometry DB:Extended --era Run2_2018 \
--python_filename NPS-X300A20wmLHEGS_1_cfg.py --fileout file:NPS-X300A20wmLHEGS_1.root \
--number 10 --no_exec --mc
```

### 

### After this we then just run the configuration file. 

cmsRun X300A20wmLHEGS\_1\_cfg.py

After this runs it should successfully give you an output root file completing the first cmsRun step. If you have errors from missing libraries move python files up one directory (with a mv or cp command).

It will be assumed that you know to run cmsRun after running cmsDriver throughout the rest of this guide.

One may want to fix LHAPDF (or other) paths if they aren't working for better runs.  

## Refining the cards

### Now is a good time to refine cards. We will match these to what Stephen did largely. One may want to apply a custom script to auto produce these for whatever signal you want to produce. You will still have to pre-run in MG to get the param\_card.dat file.

The baseline for all the cards you will need is here: [https://github.com/cms-sw/genproductions/tree/mg27x/bin/MadGraph5\_aMCatNLO/cards/production/2017/13TeV/XtoAAto4G/XtoAAto4G\_X500A5](https://github.com/cms-sw/genproductions/tree/mg27x/bin/MadGraph5_aMCatNLO/cards/production/2017/13TeV/XtoAAto4G/XtoAAto4G_X500A5)

**run\_card.dat and madspin\_card.dat will be entirely unchanged from the reference (for now).**

## proc\_card.dat 

* Change ‘add process p p \> y0 j \[QCD\] QED \= 0 @1’ to ‘add process p p \> y0 j \[noborn=QCD\] QED \= 0 @1’  
* Output name based on signal to be produced (XaaTo4G\_X\#A\#)

## extramodels.dat

* Change ‘Phi2\_simp\_tt\_qed2.zip’ to ‘Phi2\_simp\_tt\_qed.zip’  
* cd /path/to/genproductions/bin/MadGraph5\_aMCatNLO  
* mkdir models  
* Copy Phi2\_simp\_tt\_qed.zip to the /path/to/models directory

You will also need to modify gridpack\_generation.sh   
Change/comment,

* wget \--no-check-certificate https://cms-project-generators.web.cern.ch/cms-project-generators/$model

Add/replace with,

* cp $PRODHOME/models/$model .

## customizecards.dat

* First, after selecting X and Phi masses, run MG and evaluate decay widths for PID 6, 54, and 90000054 (you’ll find it in the automatically generated param\_card.dat file).  
* Set the masses of each ID to your specification  
* Set the decay widths to what MG evaluated them as.

### So basically the order is:

* Pre-run MG to populate cards  
* Modify cards (and others) as specified here  
* Create Gridpack and do cmsDriver/Run

# Generating PU

## Before we Premix we need to generate a min bias PU file. These steps are based on Garvita’s instructions. 

**We’ll start by generating a min bias file.** 
```csh
cmsDriver.py Configuration/Generator/python/MinBias_13TeV_pythia8_TuneCUETP8M1_cfi.py \
 -s GEN,SIM -n 10 --conditions auto:phase1_2018_realistic --beamspot Realistic25ns13TeVEarly2018Collision \
 --datatier GEN-SIM --eventcontent FEVTDEBUG --era Run2_2018 --relval 9000,100 \
 --python_filename MinBiasSampleFull3.py --fileout file:MinBiasFull3.root --no_exec
```

**After running that and getting its output, we then make the Premix sample.** 
```csh
 cmsDriver.py step1 --evt_type Configuration/Generator/python/SingleNuE10_cfi.py \
 -s GEN,SIM,DIGI:pdigi_valid -n 10 --conditions auto:phase1_2018_realistic \
 --datatier PREMIX --eventcontent PREMIX --procModifiers premix_stage1 \
 --era Run2_2018 --relval 100000,100 \
 --pileup AVE_35_BX_25ns --pileup_input file:MinBiasFull3_RunII2017.root \
 --python_filename MinBiasFullstep21_RunII2017.py --fileout file:MinBiasPremix_RunII2017.root --no_exec
```

# 5\. Premixing

## Now that we have our GEN-SIM step done, we have to do the Premix step. This will start with following the old simulation. 
**Originally, Stephen’s old config went roughly as follows.** 
```csh
cmsDriver.py  --eventcontent PREMIXRAW \
--customise Configuration/DataProcessing/Utils.addMonitoring \
--datatier GEN-SIM-RAW \
--conditions auto:phase1_2017_realistic \
--step DIGI,DATAMIX,L1,DIGI2RAW,HLT:@relval2017 \
--datamix PreMix \
\--era Run2_2017 \
--python_filename NPS-RunIIFall17DRPremix_1_cfg.py \
--fileout file:NPS-X300A20_Premix_1.root --filein file:NPS-X300A20wmLHEGS_1.root \
--number 10 \
--pileup_input "dbs:/Neutrino_E-10_gun/RunIISummer17PrePremix-MCv2_correctPU_94X_mc2017_realistic_v9-v1/GEN-SIM-DIGI-RAW" \
--no_exec --mc
```

## 

**This almost works, but we generated new PU so we have the following.**
```csh
cmsDriver.py  --eventcontent PREMIXRAW \
  --customise Configuration/DataProcessing/Utils.addMonitoring \
  --datatier GEN-SIM-RAW \
  --conditions auto:phase1_2018_realistic \
  --step DIGI,DATAMIX,L1,DIGI2RAW,HLT \
  --datamix PreMix \
  --era Run2_2018 \
  --procModifiers premix_stage2 \
  --python_filename NPS-RunIIFall17DRPremix_1_cfg.py \
  --fileout file:NPS-X300A20_Premix_1.root \
  --filein file:NPS-X300A20wmLHEGS_1.root \
  --number 10 \
  --pileup_input file:MinBiasPremix_RunII2018.root \
  --no_exec --mc
```

**After we have proper output from Premix \+ PU, we can then run AODSIM.**
```csh
cmsDriver.py step2 \
  --filein file:NPS-X300A20_Premix_1.root \
  --fileout file:NPS-X300A20_AODSIM_1.root \
  --conditions auto:phase1_2018_realistic \
  --step RAW2DIGI,L1Reco,RECO,RECOSIM \
  --datatier AODSIM \
  --eventcontent AODSIM \
  --era Run2_2018 \
  --mc \
  --no_exec \
  --number -1 \
  --python_filename X300A20_AODSIM_cfg_1.py
```

## After this we have effectively performed the DIGI-RECO step.

**To do this using premade PU, we have to do some extra work. Start by calling cmsDriver with the following command.**
```csh
cmsDriver.py  --eventcontent PREMIXRAW \
  --customise Configuration/DataProcessing/Utils.addMonitoring \
  --datatier GEN-SIM-RAW \
  --conditions auto:phase1_2018_realistic \
  --step DIGI,DATAMIX,L1,DIGI2RAW,HLT \
  --datamix PreMix \
  --era Run2_2018 \
  --procModifiers premix_stage2 \
  --python_filename NPS-RunIIFall17DRPremix_1_cfg.py \
  --fileout file:NPS-X300A20_Premix_1.root \
  --filein file:NPS-X300A20wmLHEGS_1.root \
  --number 10 \
  --pileup_input "dbs:/Neutrino_E-10_gun/RunIISummer20ULPrePremix-UL18_106X_upgrade2018_realistic_v11_L1v1-v2/PREMIX" \
  --no_exec --mc
```

**However, this will not work immediately. We have to filter for the files we can actually access. This method was referenced from Garvita and Gabija’s guide. Run the following commands.**
```csh
dasgoclient -query="file dataset=/Neutrino_E-10_gun/RunIISummer20ULPrePremix-UL18_106X_upgrade2018_realistic_v11_L1v1-v2/PREMIX site=T2_CH_CERN" >& premixfiles.txt
awk 'NR==1 {printf "\x27%s\x27", $0} NR>1 {printf ", \x27%s\x27", $0}' premixfiles.txt > inputfiles.txt
```

**Now we can go into the config file we made with cmsDriver and replace the line containing,**
process.mixData.input.fileNames = cms.untracked.vstring([ ])

**This will be replaced with the files dumped to inputfiles.txt**
**After doing this we can then finally run the PREMIX step and finish.**

# 6\. Slimming

### This leads us to the final stages of simulation. 
**First we will do miniAOD.**
```csh
cmsDriver.py step3 --filein file:NPS-X300A20_AODSIM_1.root --fileout file:MiniAOD2017_2.root \
--python_filename MiniAODstep2017.py \
--eventcontent MINIAODSIM --datatier MINIAODSIM --conditions auto:phase1_2018_realistic \
--step PAT --nThreads 8 --geometry DB:Extended \
--era Run2_2018 -n -1 --mc --no_exec
```

**After that, we finish with nanoAOD.**
```csh
cmsDriver.py NANO -s NANO --mc \
--conditions auto:phase1_2018_realistic --era Run2_2018,run2_nanoAOD_106Xv2 \
--eventcontent NANOAODSIM --datatier NANOAODSIM \
--customise_commands="process.add_(cms.Service('InitRootHandlers', EnableIMT = cms.untracked.bool(False)));process.MessageLogger.cerr.FwkReport.reportEvery=1000" \
--python_filename NPS-X300A20_NanoAOD_1_cfg.py \
--fileout file:NanoAOD_Test.root \
--filein file:MiniAOD2017_2.root \
-n -1 --no_exec
```

### This should mean we have successfully produced signal files.

# Summary

## If you’ve made it this far it means you’ve successfully completed making a XaaTo4G signal file. I’ll summarize the steps here for streamlining this process. 

1. Generate PU/Premix sample (Once)  
2. Define Xaa process in MG5 to create base cards  
   1. Modify Cards as needed  
   2. Copy cards where gridpack generation script can see them  
3. Create Gridpack based on your process  
4. LHEGS  
5. Premix → AODSIM  
6. MINIAOD → NANOAOD  
7. Repeat steps 2-6 for each new signal combination of Xaa

# Scaling up with HTCondor
## After one confirms they have everything working, scaling up is the next step. If you’re producing on your own, this is how you can do so. For this it works best to run on LXPLUS, so this part of the guide assumes you can do so.

First, reproduce the requirements for running cmsDriver on LXPLUS. Then we will make bash scripts for each step. I’ll show examples of how to do this for the first two steps and assume you can figure out the rest because it becomes trivial after learning the PREMIX step. 

**The following is basically the skeleton of what one needs in one of these bash scripts. In this case it’s the LHEGS step. You mainly need to ensure that you can enable your CMSSW environment, and then run the cmsDriver/cmsRun job. Much of this you can learn from looking at the McM records as well.** (*Note: Make sure your shell files are executable with chmod +x name.sh*)

```csh
#!/bin/bash

source /cvmfs/cms.cern.ch/cmsset_default.sh

# Setup CMSSW environment
cd /afs/cern.ch/user/r/rsnuggsj/CMSSW_VERSIONS/CMSSW_12_2_3/src
eval `scram runtime -sh`

# Random seed between 1 and 100 for externalLHEProducer
SEED=$(($(date +%s) % 100 + 1))

#LHEGS
cmsDriver.py Configuration/Generator/python/XaaTo4G.py  \
--eventcontent RAWSIM,LHE  --customise Configuration/DataProcessing/Utils.addMonitoring  \
--datatier GEN-SIM,LHE --conditions auto:phase1_2018_realistic  \
--beamspot Realistic25ns13TeVEarly2018Collision  \
--customise_commands process.RandomNumberGeneratorService.externalLHEProducer.initialSeed="int(${SEED})"  \
--step LHE,GEN,SIM  --geometry DB:Extended  --era Run2_2018  \
--python_filename NPS-X300A20wmLHEGS_1_cfg.py --fileout file:/eos/user/r/rsnuggsj/NPS-X300A20wmLHEGS_1.root  \
--number 10000  --no_exec --mc || exit $? ;

cmsRun NPS-X300A20wmLHEGS_1_cfg.py || exit $? ;
```
**Now, we need to make an HTCondor submission/job file. I’ll paste the LHEGS example here, and explain what’s needed/why.**
```csh
executable            = /path/to/CMSSW_VERSIONS/CMSSW_12_2_3/src/LHEGS.sh
arguments             = $(ClusterId) $(ProcId)
output                = /path/to/output/LHEGS.$(ClusterId).$(ProcId).out
error                 = /path/to/error/LHEGS.$(ClusterId).$(ProcId).err
log                   = /path/to/log/LHEGS.$(ClusterId).log
MY.WantOS             = "el7"
+JobFlavour = "testmatch"

# Use your own CMSSW area
transfer_executable   = True
should_transfer_files = YES
when_to_transfer_output = ON_EXIT

request_cpus = 1
request_memory = 10000
+RequestDisk = 10000000
queue
```
The first handful of lines are basically what’s always part of a Condor job file. We’re basically just defining where our program is and where to dump output. However, the really important bits are what comes after. 

```csh
MY.WantOS             = "el7"
```
This tells the job to prepare a slc7 environment, which is necessary for our CMSSW.
```csh
+JobFlavour = "testmatch"
```
This tells the job to run for 3 days before killing it. This will have to be set according to expectations depending on how many events you’re generating. 3 days is what it takes for LHEGS to generate 10,000 events on 1 CPU. 

The rest of this stuff just makes sure we’re using our CMSSW area and that we have enough resources to do the job. 

Save both the shell script and the job file to the running CMSSW directory (i.e. CMSSW_XYZ/src) and then you can submit the job with,

```csh
condor_submit jobfilename.sub
```
## Now, doing the PREMIX step is a little bit more work. What you’ll want to do first is go ahead and prepare the PREMIX configuration file first as prescribed earlier. 
Normally when we do this we have to initialize a proxy with something like,
```csh
voms-proxy-init --voms cms -valid 192:00
```
However, you’re going to need to copy that proxy somewhere that HTCondor can access so that it can use that proxy with your job. Make note of where that saves your proxy file when you call voms. Then, make a folder and copy it there. 
```csh
mkdir -p ~/private/x509up
cp /path/to/yourproxyfile ~/private/x509up
```
**Then you’ll want to make your shell and job files for this step.**
```csh
#!/bin/bash

export X509_USER_PROXY=$1
voms-proxy-info -all
voms-proxy-info -all -file $1
source /cvmfs/cms.cern.ch/cmsset_default.sh

# Setup CMSSW environment
cd /afs/cern.ch/user/r/rsnuggsj/CMSSW_VERSIONS/CMSSW_12_2_3/src
eval `scram runtime -sh`

#PREMIX
cmsRun NPS-X300A20_Premix_1_cfg.py || exit $? ;
```
**The extra lines here are basically just there to ensure your proxy gets passed along and loaded in for the job. Now for the job file,**
```csh
executable            = /path/to/CMSSW_12_2_3/src/PREMIX_RUN.sh
arguments             = $(Proxy_path) $(ClusterId) $(ProcId)
output                = /path/to/output/PREMIX.$(ClusterId).$(ProcId).out
error                 = /path/to/error/PREMIX.$(ClusterId).$(ProcId).err
log                   = /path/to/log/PREMIX.$(ClusterId).log
MY.WantOS             = "el7"
+JobFlavour = "testmatch"
Proxy_filename = x509up
Proxy_path = /path/to/home/private/$(Proxy_filename)

# Use your own CMSSW area
transfer_executable   = True
should_transfer_files = YES
transfer_input_files = $(Proxy_path)
when_to_transfer_output = ON_EXIT_OR_EVICT

request_cpus = 1
request_memory = 10000
+RequestDisk = 10000000
queue
```
Assuming you copied your proxy exactly as I described above, this will work. 
The rest of the steps follow simply from these instructions.

For more info on running HTCondor jobs refer to: https://batchdocs.web.cern.ch/index.html
 
x509 proxy info is here: https://batchdocs.web.cern.ch/tutorial/exercise2e_proxy.html

Change these as needed depending on your run conditions (i.e. Run2/Run3)

# Run3 Production
Run3 production will share many details with Run2, but conditions will be different.

To ensure ease of use, we will use CMMSW_13_2_9. This is because the Run3 PU available requires newer CMSSW. To use CMSSW_12_2_X would require generating one’s own PU or access to PU on tape storage.

1. ## Universal Changes

   At every stage in simulation you have to specify ‘conditions’ and ‘era’. These will have to change to reflect Run3.  
* Conditions can be for 2022 and beyond   
  * –conditions phase1\_2022\_realistic  
  * –conditions phase1\_2023\_realistic  
  * etc.

* Eras are a bit more finicky. Run3\_2022 or 2023 work in newer CMSSW. If you’re trying to stick to CMSSW\_12\_2\_X though you will need to choose just Run3. Choosing the Run3 generic tag works in general.

2. ## LHEGS

* Beamspot (--beampot) is what changes here. You can pick anything 2022 and beyond.  
  * –beamspot Realistic25ns13p6TeVEarly2023Collision  
  * In earlier CMSSW you will likely need to use a different beamspot.  
  * Refer to the VertexSmeared.py here, [https://github.com/cms-sw/cmssw/blob/CMSSW\_12\_2\_X/Configuration/StandardSequences/python/VtxSmeared.py](https://github.com/cms-sw/cmssw/blob/CMSSW_12_2_X/Configuration/StandardSequences/python/VtxSmeared.py)

3. ## PREMIX

* PU is main change here. Older CMSSW will require one to make PU as the early PU is on tape now. Use the following for newer CMSSW.  
  * /Neutrino\_E-10\_gun/Run3Summer21PrePremix-Summer23\_130X\_mcRun3\_2023\_realistic\_v13-v1/PREMIX

    

4. ## AODSIM, MINIAOD

* Only require the minimum universal changes.


5. ## NANOAOD

* The secondary Era tag is all that changes here, just follow the NanoAOD reference.  
  * –era Run3,run3\_nanoAOD\_124

## That basically covers all of the changes required to produce for Run3.
