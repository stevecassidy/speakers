import speakers.log
import argparse
import os
from speakers.features import create_idmap
from speakers.ubm import load_ubm, sufficient_stats, adapt_models, evaluate_models, plot_results

parser = argparse.ArgumentParser(description='Train speaker models on a directory of data')
parser.add_argument('dir', type=str, nargs=1, help='subdirectory of data containing audio files')

args = parser.parse_args()

datadir = args.dir[0]

print("loading...")
enrol_csv = os.path.join("data", datadir, 'enrol.csv')
enrol_idmap = create_idmap(enrol_csv)
print("Loaded enrol filenames from ", enrol_csv)

ubm = load_ubm()
print("UBM Loaded...")
sufstat = sufficient_stats(ubm, enrol_idmap, datadir)
print("Written sufficient statistics...")
speaker_models = adapt_models(ubm, sufstat)
print("Done building speaker models...")
scores = evaluate_models(ubm, speaker_models, datadir)

plot_results(datadir, scores)
