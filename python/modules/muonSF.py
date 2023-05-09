###
# Compute and store muon SFs using correctionlib.
# 
###
from __future__ import print_function
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
import correctionlib
import numpy as np

class muonSF(Module):
    def __init__(self, json, collection="Muon"):
        """Muon SF correction module.
        Parameters:
            json: the correction file
            collection: name of the collection to be corrected
        Use addCorrection() to set which factors should be added.
        """
        self.collection = collection
        self.names = []
        self.scenarios = []
        self.valtypes = []
        self.varnames = []
        self.evaluators = []
        
        # Open the JSON file, create the evaluator
        if json.endswith(".json.gz"):
            import gzip
            with gzip.open(json,'rt') as file:
                data = file.read().strip()
                self.evaluator = correctionlib.CorrectionSet.from_string(data)
        elif json.endswith(".json"):
            self.evaluator = correctionlib.CorrectionSet.from_file(json)
        else:
            print("muonSF: Invalid json file", json)
            exit(1)

    def addCorrection(self, name, scenario, valtype, varname=None) :
        """
        Call this method to add a correction factor.
        Parameters:
            name: name of the corrections, eg. 'NUM_TrackerMuons_DEN_genTracks'
            scenario: year/scenario, eg. '2016postVFP_UL'
            valtype: type of factor, eg, 'sf', 'systup', ...
            varname: branch name suffix (defaults to valtype)
        """
        if varname == None : varname = valtype
        self.names.append(name)
        self.scenarios.append(scenario)
        self.valtypes.append(valtype)
        self.varnames.append(f"{self.collection}_{varname}")
        self.evaluators.append(self.evaluator[name])
        
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree        
        for varname in self.varnames :
            self.out.branch(varname, "F", lenVar="nMuon")

    def analyze(self, event):
        etas = [min(2.39999, abs(event.Muon_eta[i])) for i in range(event.nMuon)]
        pts  = [max(15.,event.Muon_pt[i]) for i in range(event.nMuon)]

        sfs = [1.]*event.nMuon
        for ic, cname in enumerate(self.names) :
            # We cannot make a single call to evaluate passing eta, pt as arrays
            # since POG JSONS are currently provided with flow="error", so we
            # have to loop to protect for values out of binning range.
            for iMu in range(event.nMuon) :
                try:
                    sfs[iMu]=self.evaluators[ic].evaluate(self.scenarios[ic], etas[iMu], pts[iMu], self.valtypes[ic])
                except:
                    sfs[iMu] = 1.
            self.out.fillBranch(self.varnames[ic], sfs)
            
        return True


    
