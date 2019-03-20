import speakers.log
from speakers.features import extract_features
from speakers.config import configinit, config
import json
import sys

configinit('config.ini')

if __name__ == '__main__':

    extract_features(config('UBM_DATA_DIR'))
