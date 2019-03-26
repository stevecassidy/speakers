Speaker Identification with Sidekit and Alveo
===============================

This project contains code to train and apply speaker models using the 
SIDEKIT toolkit and data derived from the Alveo Virtual Laboratory. 

## Sidekit Patch

There is a bug in the current version (1.2.3) of SIDEKIT that prevents
this code running. It is using numpy.zeros to generate a list of zeros as 
channel numbers but doesn't set the type and so gets floats by default. 
These are then used to index an array causing a crash.  

The file features_server.py is a patched version that fixes this issue. 
Copy it into the sidekit distribution before running this code. If you are 
using a virtualenv then this is <venv>/lib/python3.6/site-packages/sidekit/feature_server.py 

## Configuration

Copy config.ini.dist to config.ini and modify the settings in that file.

## Scripts

Starting with speakers.csv downloaded from austalk-query.apps.alveo.edu.au we first partition
speakers into different sets: dev, eval, test and ubm. The first three contain 50 male and 50 female
speakers each, the last (ubm) contains all remaining speakers.  The results are written to separate
text files in the `data` directory.

```commandline
python -m scripts.partition_speakers  
```

Then find the target utterances for each speaker, these are defined by `UBM_AUSTALK_COMPONENT` and
`DEV_AUSTALK_COMPONENT` in the config file.  All items for these components will be found and stored
in JSON files.  The script writes one JSON file for each set into the `data` directory, e.g. `data/dev-sentences.json`.

```commandline
python -m scripts.find_utterances
``` 

Next download the data from Alveo for the target speakers, this script takes one or more JSON filenames
as input and writes data to a corresponding directory in `data/`, eg. `data/dev-sentences.json` writes to `data/dev-sentences`

```commandline
python -m scripts.download_data json [json ...] 
```

Then compute features for the audio data. This script writes one feature file (`.h5`) for each audio file.  Arguments
are the names of the sub-directories containing the data inside the `data/` directory, eg. `dev-sentences`.

```commandline
python -m scripts.extract_features dirname [dirname ...]
```

Now train the UBM on this data

```commandline
python -m scripts.train_ubm
```

