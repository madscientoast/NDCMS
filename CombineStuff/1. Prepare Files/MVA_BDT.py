import ROOT
from ROOT import TMVA, TFile, TCut

# Initialize TMVA output file
output_file = TFile("TMVA_BDT_output_ALL.root", "RECREATE")

# Initialize TMVA factory
factory = TMVA.Factory(
    "TMVAClassification",
    output_file,
    "!V:!Silent:Color:DrawProgressBar:Transformations=I;D:AnalysisType=Classification"
)

# Create DataLoader
dataLoader = TMVA.DataLoader("dataset")

# Add variables (these should match the branches in your ROOT files)
dataLoader.AddVariable("m_asym", "F")
dataLoader.AddVariable("deltaEta", "F")
dataLoader.AddVariable("dR1", "F")
dataLoader.AddVariable("dR2", "F")

# Load signal and background files
signal_file = TFile("signal15.root")
signal_file2 = TFile("signal30.root")
signal_file3 = TFile("signal75.root")
background_file = TFile("bkg.root")

signal_tree = signal_file.Get("Events")
signal_tree2 = signal_file2.Get("Events")
signal_tree3 = signal_file3.Get("Events")
background_tree = background_file.Get("Events")

#set up weights
# Total number of signal events
N15 = 12153
N30 = 525
N75 = 109
N_total = N15 + N30 + N75

# Assign weights inversely proportional to the event count
w15 = N_total / N15  # = (12553 + 592 + 144) / 12553
w30 = N_total / N30  # = (12553 + 592 + 144) / 592
w75 = N_total / N75  # = (12553 + 592 + 144) / 144




# Add signal trees with proper weights
dataLoader.AddSignalTree(signal_tree, w15)
dataLoader.AddSignalTree(signal_tree2, w30)
dataLoader.AddSignalTree(signal_tree3, w75)
dataLoader.AddBackgroundTree(background_tree)

# Optionally, define cuts for signal and background
signalCut = TCut("")  # No cuts for now, but you can add them here
backgroundCut = TCut("")  # No cuts for now, but you can add them here

# Prepare the data for training and testing
dataLoader.PrepareTrainingAndTestTree(
    signalCut,
    backgroundCut,
    "nTrain_Signal=0:nTrain_Background=0:SplitMode=Random:NormMode=NumEvents:!V"
)

# Book a BDT method
factory.BookMethod(
    dataLoader,
    TMVA.Types.kBDT,
    "BDT",
    "!V:NTrees=200:MaxDepth=3:BoostType=AdaBoost:AdaBoostBeta=0.5:SeparationType=GiniIndex:nCuts=100"
)

# Train, test, and evaluate the model
factory.TrainAllMethods()
factory.TestAllMethods()
factory.EvaluateAllMethods()

# Save the TMVA output file
output_file.Close()

print("TMVA training complete. Results saved in TMVA_BDT_output_TEST.root")
