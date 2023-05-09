#!/usr/bin/env python3
###
# This is an example of configuring and calling a generic correctionlib module.
# Notes:
# For the sake of speed, it is important to apply a preselection whenever possible.
# Also, it is advisable to insert correction modules like this after modules
# that apply selections, so that corrections are not computed for events that
# are then discarded.
###

from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor
from PhysicsTools.NanoAODTools.modules.muonSF import *

import os
import sys
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True


### Set up the muon correction module
muSF = muonSF("POG/MUO/2016postVFP_UL/muon_Z.json.gz")
# Add TrackerMuon Reconstruction UL scale factor
muSF.addCorrection("NUM_TrackerMuons_DEN_genTracks", "2016postVFP_UL", "sf")
# Add Medium ID UL scale factor, down variation
muSF.addCorrection("NUM_MediumID_DEN_TrackerMuons", "2016postVFP_UL", "systdown", "sfsysdn")
# Add Medium ID UL scale factor, up variation
muSF.addCorrection("NUM_MediumID_DEN_TrackerMuons", "2016postVFP_UL", "systup", "sfsysup")

fnames = ["root://cms-xrd-global.cern.ch//store/mc/RunIISummer20UL16NanoAODv9/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/NANOAODSIM/20UL16JMENano_106X_mcRun2_asymptotic_v17-v1/2820000/11061525-9BB6-F441-9C12-4489135219B7.root"]

p = PostProcessor(".", fnames, "nMuon>=2", None, [muSF], provenance=True, prefetch=True, longTermCache=True,)
p.run()
