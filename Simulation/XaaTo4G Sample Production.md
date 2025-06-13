# 4\. GEN-SIM

### Now that we have a gridpack, we can start the rest of the simulation process. By means of DAS or MCM one can track down the old simulation commands ([https://cms-pdmv-prod.web.cern.ch/mcm/requests?dataset\_name=XtoAAto4G\_X300A15\_TuneCP5\_13TeV-madgraph-pythia8\&page=0\&shown=127](https://cms-pdmv-prod.web.cern.ch/mcm/requests?dataset_name=XtoAAto4G_X300A15_TuneCP5_13TeV-madgraph-pythia8&page=0&shown=127))

### This chain starts at LHEGS (i.e. LHE \+ GEN-SIM), so click the second button and you’ll see what commands are required. Inside you’ll see a curl command which will point you to where the original code fragment required to run this with cmsDriver/cmsRun. Grab that and change just the gridpack tarball it refers to, to your own. 

args \= cms.vstring('/path/to/genproductions/bin/MadGraph5\_aMCatNLO/XaaTo4G\_X300A20\_el9\_amd64\_gcc11\_CMSSW\_13\_2\_9\_tarball.tar.xz')

### Alternatively, you can also grab a version of the file off of my github. 

[(https://github.com/madscientoast/NDCMS/blob/master/Simulation/XaaTo4G.py)](https://github.com/madscientoast/NDCMS/blob/master/Simulation/XaaTo4G.py)

### From the same reference we will then run mostly the same cmsDriver command, but slightly modified so that it doesn’t spit errors at us. 

| export SEED=$(($(date \+%s) % 100 \+ 1))cmsDriver.py Configuration/Generator/python/your\_fragment.py \--eventcontent RAWSIM,LHE \--customise Configuration/DataProcessing/Utils.addMonitoring \--datatier GEN-SIM,LHE \--conditions auto:phase1\_2018\_realistic\--beamspot Realistic25ns13TeVEarly2018Collision \--customise\_commands process.RandomNumberGeneratorService.externalLHEProducer.initialSeed="int(${SEED})" \--step LHE,GEN,SIM \--geometry DB:Extended \--era Run2\_2018 \--python\_filename NPS-X300A20wmLHEGS\_1\_cfg.py \--fileout file:NPS-X300A20wmLHEGS\_1.root \--number 10 \--no\_exec \--mc |
| :---- |

### 

### After this we then just run the configuration file. 

cmsRun X300A20wmLHEGS\_1\_cfg.py

After this runs it should successfully give you an output root file completing the first cmsRun step. If you have errors from missing libraries move python files up one directory (with a mv or cp command).

It will be assumed that you know to run cmsRun after running cmsDriver throughout the rest of this guide.

One may want to fix LHAPDF (or other) paths for better runs.  
Note for later: Add Stephen’s old parton level cuts and other stuff from his run card.

### 