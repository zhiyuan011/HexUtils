# import ROOT in batch mode
import sys
import os
import argparse
oldargv = sys.argv[:]
sys.argv = [ '-b-' ]
from ROOT import *
gROOT.SetBatch(True)
sys.argv = oldargv
gStyle.SetOptStat(0)
gStyle.SetOptFit(1)

# load FWLite C++ libraries
gSystem.Load("libFWCoreFWLite.so")
gSystem.Load("libDataFormatsFWLite.so")
FWLiteEnabler.enable()

# load FWlite python libraries
from DataFormats.FWLite import Handle, Events

import tqdm

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--files", nargs="+", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("-x", "--fromXrootD", action="store_true")
    args = parser.parse_args()
    
    files = []
    for file in args.files:
        if not os.path.exists(file) and not args.fromXrootD:
            raise FileNotFoundError(f"{file} not found!")
        
        if args.fromXrootD:
            files.append(f"root://cmsxrootd.fnal.gov//{file}")
        else:
            files.append(os.path.abspath(file))

    handle_LHE, LHE_label = Handle ("LHEEventProduct"), ("externalLHEProducer")
    
    f = open(args.output, "w+")
    
    for file in files:
        LHE_event = Events([file])
        
        for i, LHE in tqdm.tqdm(enumerate(LHE_event)):
            LHE.getByLabel(LHE_label, handle_LHE)
            gen_LHE = handle_LHE.product()
            f.write("".join(list(gen_LHE)))
    
    f.close()
