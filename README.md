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

## Run an experiment

Run experiment.py

