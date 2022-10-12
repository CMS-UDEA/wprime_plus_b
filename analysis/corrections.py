import json
import correctionlib
import importlib.resources
import awkward as ak
import numpy as np
import pickle as pkl
from typing import Type
from coffea import processor, hist, util
from coffea.analysis_tools import Weights


# CorrectionLib files are available from
POG_CORRECTION_PATH = "/cvmfs/cms.cern.ch/rsync/cms-nanoAOD/jsonpog-integration"

# summary of pog scale factors: https://cms-nanoaod-integration.web.cern.ch/commonJSONSFs/
POG_JSONS = {
    "muon": ["MUO", "muon_Z.json.gz"],
    "electron": ["EGM", "electron.json.gz"],
    "pileup": ["LUM", "puWeights.json.gz"],
    "btag": ["BTV", "btagging.json.gz"],
}

POG_YEARS = {
    "2016": "2016postVFP_UL",
    "2016APV": "2016preVFP_UL",
    "2017": "2017_UL",
    "2018": "2018_UL",
}

TAGGER_BRANCH = {
    "deepJet": "btagDeepFlavB",
    "deepCSV": "btagDeep",
}


def get_pog_json(json_name: str, year: str) -> str:
    """
    returns the path to the pog json file

    Parameters:
    -----------
        json_name:
            json name (muon, electron, pileup or btag)
        year:
            dataset year
    """
    if json_name in POG_JSONS:
        pog_json = POG_JSONS[json_name]
    else:
        print(f"No json for {json_name}")
    return f"{POG_CORRECTION_PATH}/POG/{pog_json[0]}/{POG_YEARS[year]}/{pog_json[1]}"


def add_pileup_weight(weights, year, mod, nPU):
    """
    add pileup weight

    Parameters:
    -----------
        weights:
            Weights object from coffea.analysis_tools
        year:
            dataset year
        mod:
            year modifier ("" or "APV")
        nPU:
            number of true interactions (events.Pileup.nPU)
    """
    # correction set
    cset = correctionlib.CorrectionSet.from_file(
        get_pog_json(json_name="pileup", year=year + mod)
    )

    year_to_corr = {
        "2016": "Collisions16_UltraLegacy_goldenJSON",
        "2017": "Collisions17_UltraLegacy_goldenJSON",
        "2018": "Collisions18_UltraLegacy_goldenJSON",
    }

    values = {}
    values["nominal"] = cset[year_to_corr[year]].evaluate(nPU, "nominal")
    values["up"] = cset[year_to_corr[year]].evaluate(nPU, "up")
    values["down"] = cset[year_to_corr[year]].evaluate(nPU, "down")

    # add weights (for now only the nominal weight)
    weights.add("pileup", values["nominal"], values["up"], values["down"])


class BTagCorrector:
    def __init__(
        self,
        sf: str = "comb",
        wp: str = "M",
        tagger: str = "deepJet",
        year: str = "2017",
        mod: str = "",
    ):
        """
        BTag corrector object

        Parameters:.coffea
        -----------
            sf:
                scale factors to use (mujets or comb)
            wp:
                worging point (L, M or T)
            tagger:
                tagger (deepJet or deepCSV)
            year:
                dataset year
            mod:
                year modifier ("" or "APV")
        """
        self._sf = sf
        self._year = year + mod
        self._tagger = tagger
        self._wp = wp
        self._branch = TAGGER_BRANCH[tagger]

        # btag working points (only for deepJet)
        # https://twiki.cern.ch/twiki/bin/viewauth/CMS/BtagRecommendation
        with open("/home/cms-jovyan/wprime_plus_b/data/btagWPs.json", "rb") as handle:
            btagWPs = json.load(handle)
        self._btagwp = btagWPs[tagger][year + mod][wp]

        # correction set
        self._cset = correctionlib.CorrectionSet.from_file(
            get_pog_json(json_name="btag", year=year + mod)
        )

        # efficiency lookup
        self.efflookup = util.load(
            f"/home/cms-jovyan/wprime_plus_b/data/btageff_{self._tagger}_{self._wp}_{self._year}.coffea"
        )

    def btag_SF(self, j, syst="central"):
        # syst: central, down, down_correlated, down_uncorrelated, up, up_correlated
        # until correctionlib handles jagged data natively we have to flatten and unflatten
        j, nj = ak.flatten(j), ak.num(j)
        sf = self._cset[f"{self._tagger}_{self._sf}"].evaluate(
            syst,
            self._wp,
            np.array(j.hadronFlavour),
            np.array(abs(j.eta)),
            np.array(j.pt),
        )
        return ak.unflatten(sf, nj)

    def add_btag_weight(self, jets: ak.Array, weights: Type[Weights]):
        """
        Adding SF

        Parameters:
        -----------
            jets:
                jets selected in your analysis
            weights:
                Weights object from coffea.analysis_tools
        """
        # bjets (hadron flavor definition: 5=b, 4=c, 0=udsg)
        bjets = jets[(jets.hadronFlavour > 0) & (abs(jets.eta) < 2.5)]

        # b-tag efficiency
        bEff = self.efflookup(bjets.hadronFlavour, bjets.pt, abs(bjets.eta))

        # b-tag nominal scale factors
        bSF = self.btag_SF(bjets, "central")

        # mask for events passing the btag working point
        bPass = bjets[self._branch] > self._btagwp

        # tagged SF = SF*eff / eff = SF
        tagged_sf = ak.prod(bSF[bPass], axis=-1)
        # untagged SF = (1 - SF*eff) / (1 - eff)
        untagged_sf = ak.prod(((1 - bSF * bEff) / (1 - bEff))[~bPass], axis=-1)

        # combine eff and SF as tagged SF * untagged SF
        nominal_weight = ak.fill_none(tagged_sf * untagged_sf, 1.0)

        # add nominal weight
        weights.add("btagSF", nominal_weight)
