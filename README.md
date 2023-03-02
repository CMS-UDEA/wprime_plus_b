# W' + b

- [Processors](#Processors)
    * [Trigger Efficiency Processor](#Trigger-Efficiency-Processor)
    * [TTBar Control Region Processor](#TTBar-Control-Region-Processor)
- [How to run](#How-to-run)
    * [Submitting Condor jobs](#Submitting-Condor-jobs)
- [Scale factors](#Scale-factors)
- [Setting up coffea environments](#Setting-up-coffea-environments)
- [Data fileset](#Data-fileset)
    * [Re-making the input dataset files with DAS](#Re-making-the-input-dataset-files-with-DAS)
    * [Luminosity](#luminosity)

[![Codestyle](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

<p align="left">
  <img width="300" src="https://i.imgur.com/OWhX13O.jpg" />
</p>

Python package for analyzing W' + b in the electron and muon channels. The analysis uses a columnar framework to process input tree-based [NanoAOD](https://twiki.cern.ch/twiki/bin/view/CMSPublic/WorkBookNanoAOD) files using the [coffea](https://coffeateam.github.io/coffea/) and [scikit-hep](https://scikit-hep.org) Python libraries.



## Processors

The processor object is where all of the analysis is defined. Here we define two processors:

### [Trigger Efficiency Processor](processors/trigger_efficiency_processor.py) 

Processor use to compute trigger efficiencies. 

The processor applies the following pre-selection cuts





| $$\textbf{Object}$$    | $$\textbf{Variable}$$          | $$\textbf{Cut}$$                                                    | 
| ---------------------  | ------------------------------ | ------------------------------------------------------------------- |
| $$\textbf{Electrons}$$ |                                |                                                                     |
|                        | $p_T$                        | $\geq 30$ GeV                                           |
|                        | $\eta$                       | $\| \eta \| < 1.44$ and $1.57 < \| \eta \| < 2.5$       |
|                        | pfRelIso04_all                 | $\lt 0.25$                                                        |
|                        | mvaFall17V2Iso_WP80 (ele) mvaFall17V2Iso_WP90 (mu) | $\text{True}$|
| $$\textbf{Muons}$$     |                                |                                                                     |
|                        | $p_T$                        | $\geq 30$ GeV                                          |
|                        | $\eta$                       | $\lt 2.4$                                                 |
|                        | pfRelIso04_all       | $\lt 0.25$                                                        |
|                        | mediumId (ele) tightId (mu) | $\text{True}$                   |
| $$\textbf{Jets}$$      |                                |                                                                     |
|                        | $p_T$                        |  $\geq 20$ GeV                                       |
|                        | $\eta$                       | $\lt 2.4$                                                 |
|                        | JetId                        | $6$                                                               |
|                        | puId                          | $7$                                                               |
|                        | btagDeepFlavB                | $\gt$ Medium WP                                          |



The trigger efficiency is computed as:


$$\epsilon = \frac{\text{selection cuts and reference trigger and main trigger}}{\text{selection cuts and reference trigger}}$$


so we define two regions for each channel: ```numerator``` and ```denominator```. We use the following triggers:


$\text{Analysis triggers}$


| Channel        | 2016           |    | 2017           |   | 2018           |
|----------------|----------------|--- |----------------|---|----------------|
| Muon           | IsoMu24        |    | IsoMu27        |   | IsoMu24        |
| Electron       | Ele27\_WPTight\_Gsf |   | Ele35\_WPTight\_Gsf |   | Ele32\_WPTight\_Gsf |


The reference and main triggers, alongside the selection criteria applied to establish each region, are presented in the following tables:


#### Electron channel

| Trigger        | 2016           |   | 2017           |   | 2018           |
|----------------|----------------|---|----------------|---|----------------|
| Reference trigger   | IsoMu24        |   | IsoMu27        |   | IsoMu24        |
| Main trigger         | Ele27\_WPTight\_Gsf |   | Ele35\_WPTight\_Gsf |   | Ele32\_WPTight\_Gsf |


| Selection cuts      | 
| ---------------------------------|
| Luminosity calibration            |
| MET filters                       |
| $N(bjet) \geq 1$                   |
| $N(\mu) = 1$                      |
| $N(e) = 1$                       |

#### Muon channel

| Trigger        | 2016           |   | 2017           |   | 2018           |
|----------------|----------------|---|----------------|---|----------------|
| Reference trigger         | Ele27\_WPTight\_Gsf |   | Ele35\_WPTight\_Gsf |   | Ele32\_WPTight\_Gsf |
| Main trigger   | IsoMu24        |   | IsoMu27        |   | IsoMu24        |



| Selection cuts      | 
| ------------------------------------------------------------------- |
| Luminosity calibration                                    |
| MET filters                        |
| $\Delta R (\mu, bjet) \gt 0.4$                           |
| $N(bjet) \geq 1$                           |
| $N(\mu) = 1$                        |
| $N(e) = 1$                       |


### [TTBar Control Region Processor](processors/ttbar_processor.py) 

Processor use to estimate backgrounds in a $t\bar{t}$ control region. 

The processor applies the following pre-selection cuts

| $$\textbf{Object}$$    | $$\textbf{Variable}$$          | $$\textbf{Cut}$$                                                    | 
| ---------------------  | ------------------------------ | ------------------------------------------------------------------- |
| $$\textbf{Electrons}$$ |                                |                                                                     |
|                        | $p_T$                        | $\geq 30$ GeV                                        |
|                        | $\eta$                       | $\| \eta \| < 1.44$ and $1.57 < \| \eta \| < 2.5$       |
|                        | pfRelIso04_all                 | $\lt 0.25$                                                        |
|                        | mvaFall17V2Iso_WP80 (ele) mvaFall17V2Iso_WP90 (mu) | $\text{True}$|
| $$\textbf{Muons}$$     |                                |                                                                     |
|                        | $p_T$                        | $\geq 30$ GeV                                         |
|                        | $\eta$                       | $\lt 2.4$                                                 |
|                        | pfRelIso04_all               | $\lt 0.25$                                                        |
|                        | tightId                      | $\text{True}$                   |
| $$\textbf{Taus}$$      |                                |                                                                     |
|                        | $p_T$                        | $\geq 20$ GeV                                               |
|                        | $\eta$                       | $\lt 2.3$                                                 |
|                        | $dz$                         | $\lt 0.2$                                                        | 
|                        | idDeepTau2017v2p1VSjet       | $\gt 8$                                                           |
|                        | idDeepTau2017v2p1VSe         | $\gt 8$                                                           |
|                        | idDeepTau2017v2p1VSmu        | $\gt 1$                                                           |
| $$\textbf{Jets}$$      |                                |                                                                     |
|                        | $p_T$                        |  $\geq 20$ GeV                                            |
|                        | $\eta$                       | $\lt 2.4$                                                 |
|                        | JetId                        | $6$                                                               |
|                        | puId                          | $7$                                                               |
|                        | btagDeepFlavB                | $\gt$ Medium WP                                          |



and additional selection cuts for each channel:

#### Electron channel

| Selection cuts      | 
| ---------------------------------|
| Electron Trigger      |
| Luminosity calibration                  |
| MET filters           |
| $p_T^{miss}\gt 50$ GeV |
| $N(bjet) = 2$                  |
| $N(\tau) = 0$                  |
| $N(\mu) = 0$                   |
| $N(e) = 1$                    |




#### Muon channel


| Selection cuts      | 
| ---------------------------------|
| Muon Trigger          |
| Luminosity calibration                  |
| MET filters           |
| $\Delta R (\mu, bjet) \gt 0.4$ |
| $p_T^{miss}\gt 50$ GeV |
| $N(bjet) = 2$                  |
| $N(\tau) = 0$                  |
| $N(e) = 0$                     |
| $N(\mu) = 1$                   |



## How to run

From within this repo, you can run the uproot job that will produce coffea output files. To see a list of arguments needed to run this program please enter the following in the terminal:

```bash
python run.py --help
```
The output should look something like this:

```
usage: run.py [-h] [--sample SAMPLE] [--workers WORKERS] [--channel CHANNEL] [--processor PROCESSOR] [--executor EXECUTOR] [--nfiles NFILES] [--year YEAR] [--yearmod YEARMOD]
              [--output_location OUTPUT_LOCATION]

optional arguments:
  -h, --help            show this help message and exit
  --sample SAMPLE       sample to process (see data/simplified_samples.json values)
  --workers WORKERS     number of workers for the futures executor (default 4)
  --channel CHANNEL     lepton channel {ele, mu}
  --processor PROCESSOR
                        processor to run {trigger, ttbar}
  --executor EXECUTOR   executor {iterative, futures, dask}
  --nfiles NFILES       number of files per sample (default 1. To run all files use -1)
  --year YEAR           year
  --yearmod YEARMOD     year modifier {'', 'APV'}
  --output_location OUTPUT_LOCATION
                        output location (default ./outfiles)
```

The `run.py` file executes the desired processor with user-selected options. By running this file, the analysis is performed and the results are stored in the `OUTPUT_LOCATION` directory, defined by the `--output_location` flag. 

To run the desired processor, use the `--processor` flag and specify either `trigger` or `ttbar`. Select the electron (ele) or muon (mu) channel with the `--channel` flag. The dataset can be selected using `--sample`, followed by the name of the dataset you want to run. The available options can be found in `data/simplified_samples.json`.

To select the number of `.root` files to load, use the `--nfiles` option. The year can be selected using the `--year` flag, and the `--yearmod` flag is used to specify whether the dataset uses APV or not.

Three executors are available: `iterative`, `futures`, and `dask`. The `iterative` executor uses a single worker, while the `futures` executor uses the number of workers specified by the `--workers` flag. The `dask` executor uses Dask functionalities to scale up the analysis.

Let's assume we are using [Coffea-Casa](https://coffea-casa.readthedocs.io/en/latest/cc_user.html) and we want to perform the analysis for the 2017 run.

To test locally first, can do e.g.:

```bash
python run.py --processor ttbar --channel ele --sample TTTo2L2Nu --executor iterative --year 2017 --nfiles 1 
```

To scale up the analysis using Dask type:

```bash
python run.py --processor ttbar --channel ele --sample TTTo2L2Nu --executor dask --year 2017 --nfiles -1 
```

#### Notes: 
* Currently, the processors are only functional for the year 2017. 
* Coffea-Casa is faster and more convenient, however still somewhat experimental so for large of inputs and/or processors which may require heavier cpu/memory Condor is recommended (see next section).

### Submitting Condor jobs

To do


## Scale factors

We use the common json format for scale factors (SF), hence the requirement to install [correctionlib](https://github.com/cms-nanoAOD/correctionlib). The SF themselves can be found in the central [POG repository](https://gitlab.cern.ch/cms-nanoAOD/jsonpog-integration), synced once a day with CVMFS: `/cvmfs/cms.cern.ch/rsync/cms-nanoAOD/jsonpog-integration`. A summary of their content can be found [here](https://cms-nanoaod-integration.web.cern.ch/commonJSONSFs/). The SF implemented are (See [corrections](processors/corrections.py)):

* Pileup
* btagging
* Electron ID
* Electron Reconstruction
* Electron Trigger*
* Muon ID
* Muon Iso
* Muon Trigger (Iso)
* MET 

*The use of these scale factors are not by default approved from EGM. We are using the scale factors derived by Siqi Yuan https://twiki.cern.ch/twiki/bin/viewauth/CMS/EgHLTScaleFactorMeasurements


## Setting up coffea environments

#### Install miniconda (if you do not have it already)
In your lxplus area:
```
# download miniconda
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh

# run and follow instructions  
bash Miniconda3-latest-Linux-x86_64.sh

# Make sure to choose `yes` for the following one to let the installer initialize Miniconda3
# > Do you wish the installer to initialize Miniconda3
# > by running conda init? [yes|no]
```
Verify the installation is successful by running conda info and check if the paths are pointing to your Miniconda installation. 
If you cannot run conda command, check if you need to add the conda path to your PATH variable in your bashrc/zshrc file, e.g.,
```
export PATH="$HOME/nobackup/miniconda3/bin:$PATH"
```
To disable auto activation of the base environment:
```
conda config --set auto_activate_base false
```

#### Set up a conda environment and install the required packages
```
# create a new conda environment
conda create -n coffea-env python=3.8

# activate the environment
conda activate coffea-env

# install packages
pip install numpy pandas coffea correctionlib pyarrow

# install xrootd
conda install -c conda-forge xrootd
```

## Data fileset

The fileset json files that contain a dictionary of the files per sample are in the `data/fileset` directory.

#### Re-making the input dataset files with DAS

```
# connect to lxplus with a port forward to access the jupyter notebook server
ssh <your_username>@lxplus.cern.ch localhost:8800 localhost:8800

# create a working directory and clone the repo (if you have not done yet)
git clone https://github.com/deoache/wprime_plus_b

# enable the coffea environment
conda activate coffea-env

# then activate your proxy
voms-proxy-init --voms cms --valid 100:00

# activate cmsset
source /cvmfs/cms.cern.ch/cmsset_default.sh

# open the jupyter notebook on a browser
cd data/fileset/
jupyter notebook --no-browser --port 8800
```

there should be a link looking like `http://localhost:8800/?token=...`, displayed in the output at this point, paste that into your browser.
You should see a jupyter notebook with a directory listing.

Open `filesetDAS.ipynb` and run it. The json files containing the datasets to be run should be saved in the same `data/fileset/` directory.

We use the recomended Run-2 UltraLegacy Datasets. See https://twiki.cern.ch/twiki/bin/view/CMS/PdmVRun2LegacyAnalysis


#### Luminosity

See luminosity recomendations for Run2 at https://twiki.cern.ch/twiki/bin/view/CMS/LumiRecommendationsRun2. To obtain the integrated luminosity type (on lxplus):

```
export PATH=$HOME/.local/bin:/afs/cern.ch/cms/lumi/brilconda-1.1.7/bin:$PATH
pip uninstall brilws
pip install --install-option="--prefix=$HOME/.local" brilws
```

* SingleMuon: type

```
brilcalc lumi -b "STABLE BEAMS" --normtag /cvmfs/cms-bril.cern.ch/cms-lumi-pog/Normtags/normtag_PHYSICS.json -u /fb -i /afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions17/13TeV/Legacy_2017/Cert_294927-306462_13TeV_UL2017_Collisions17_GoldenJSON.txt --hltpath HLT_IsoMu27_v*
```

output:
```
#Summary: 
+-----------------+-------+------+--------+-------------------+------------------+
| hltpath         | nfill | nrun | ncms   | totdelivered(/fb) | totrecorded(/fb) |
+-----------------+-------+------+--------+-------------------+------------------+
| HLT_IsoMu27_v10 | 13    | 36   | 8349   | 2.007255669       | 1.870333304      |
| HLT_IsoMu27_v11 | 9     | 21   | 5908   | 1.383159994       | 1.254273727      |
| HLT_IsoMu27_v12 | 47    | 122  | 46079  | 8.954672794       | 8.298296788      |
| HLT_IsoMu27_v13 | 91    | 218  | 124447 | 27.543983745      | 26.259684708     |
| HLT_IsoMu27_v14 | 2     | 13   | 4469   | 0.901025085       | 0.862255849      |
| HLT_IsoMu27_v8  | 2     | 3    | 1775   | 0.246872270       | 0.238466292      |
| HLT_IsoMu27_v9  | 11    | 44   | 14260  | 2.803797063       | 2.694566730      |
+-----------------+-------+------+--------+-------------------+------------------+
#Sum delivered : 43.840766620
#Sum recorded : 41.477877399
```

* SingleElectron: type

```
brilcalc lumi -b "STABLE BEAMS" --normtag /cvmfs/cms-bril.cern.ch/cms-lumi-pog/Normtags/normtag_PHYSICS.json -u /fb -i /afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions17/13TeV/Legacy_2017/Cert_294927-306462_13TeV_UL2017_Collisions17_GoldenJSON.txt --hltpath HLT_Ele35_WPTight_Gsf_v*
```
output:

```
#Summary: 
+--------------------------+-------+------+--------+-------------------+------------------+
| hltpath                  | nfill | nrun | ncms   | totdelivered(/fb) | totrecorded(/fb) |
+--------------------------+-------+------+--------+-------------------+------------------+
| HLT_Ele35_WPTight_Gsf_v1 | 2     | 3    | 1775   | 0.246872270       | 0.238466292      |
| HLT_Ele35_WPTight_Gsf_v2 | 11    | 44   | 14260  | 2.803797063       | 2.694566730      |
| HLT_Ele35_WPTight_Gsf_v3 | 13    | 36   | 8349   | 2.007255669       | 1.870333304      |
| HLT_Ele35_WPTight_Gsf_v4 | 9     | 21   | 5908   | 1.383159994       | 1.254273727      |
| HLT_Ele35_WPTight_Gsf_v5 | 20    | 66   | 22775  | 5.399580877       | 4.879405647      |
| HLT_Ele35_WPTight_Gsf_v6 | 27    | 56   | 23304  | 3.555091917       | 3.418891141      |
| HLT_Ele35_WPTight_Gsf_v7 | 93    | 231  | 128916 | 28.445008830      | 27.121940558     |
+--------------------------+-------+------+--------+-------------------+------------------+
#Sum delivered : 43.840766620
#Sum recorded : 41.477877399
```