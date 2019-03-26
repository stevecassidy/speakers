import speakers.log
import argparse
from speakers.features import extract_features

parser = argparse.ArgumentParser(description='Compute features for audio files')
parser.add_argument('dir', type=str, nargs='+', help='subdirectory of data containing audio files')

args = parser.parse_args()

for dir in args.dir:
    extract_features(dir)
