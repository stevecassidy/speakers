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

## Data Preparation and Download

This section covers the creation of the training and testing datasets from the Austalk collection
stored on Alveo and so it is specific to this collection.  Later sections should work on any collection
using a similar directory layout. 

To develop a speaker id/verification system we need some different data collections:

* a large collection of speakers to use for generating a Universal Background Model (UBM), this should 
be phonetically diverse and include a range of speakers
* For development we need two data sets. One for repeated experimentation while we develop the 
models and tune parameters (dev), one to test a tuned model to see how it performs
on unseen data (test) and a final one that is kept back until all tuning has been done for a
final evaluation (eval).   Each of these sets contain different speakers sampled from the overall
speaker set.
* Within each set we have for each speaker a set of enrollment data and some test data.  Enrollment
data is used to create models for each speaker. Test data is used to evaluate the speaker id or 
verification performance of the model.  


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

Script to define enrol/test subsets for a given directory.  Outputs two csv files with speaker labels and basename pairs 
ready to be used in training and testing later.  Files are written to the data directory with names `enrol.csv` and
`test.csv`.

```commandline
python -m scripts.split_enrollment dir
```

### Feature Extraction


Then compute features for the audio data. This script writes one feature file (`.h5`) for each audio file.  Arguments
are the names of the sub-directories containing the data inside the `data/` directory, eg. `dev-sentences`.

```commandline
python -m scripts.extract_features ubm-sentences dev-sentences
```


### Model training


Now train the UBM on the UBM data set:

```commandline
python -m scripts.train_ubm
```

We can now build speaker models, this will use a different dataset containing the speakers we wish
to recognise or verify. 

```commandline
python -m scripts.train_speaker_models dev-sentences
```

### Testing

Finally we can test the models and generate a DET plot:

```commandline
python -m scripts.train_speaker_models dev-sentences
```

This will output a score (EER and minDCF) and generate a PDF plot in the current directory.



