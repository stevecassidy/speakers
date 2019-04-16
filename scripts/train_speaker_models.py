import speakers.log
import argparse
import os
from speakers.features import create_idmap
from speakers.ubm import load_ubm, sufficient_stats, adapt_models, evaluate_models, plot_results
from speakers.config import configinit, config

configinit('config.ini')

parser = argparse.ArgumentParser(description='Train speaker models on a directory of data')
parser.add_argument('set', type=str, nargs=1, help='data set name to use, eg. dev, test, eval')

args = parser.parse_args()

dataset = args.dir[0]

for gender in ['male', 'female']:

    datadir = dataset + '-' + gender + '-' + config('DEV_AUSTALK_COMPONENT')

    print('loading', gender, 'data')
    enrol_csv = os.path.join("data", datadir, 'enrol.csv')
    enrol_idmap = create_idmap(enrol_csv)
    print("Loaded enrol filenames from ", enrol_csv)

    ubm = load_ubm(gender)
    print("UBM Loaded...")
    sufstat = sufficient_stats(ubm, enrol_idmap, datadir)
    print("Written sufficient statistics...")
    speaker_models = adapt_models(ubm, sufstat, datadir)
    print("Done building speaker models...")
    scores = evaluate_models(ubm, speaker_models, datadir)

    plot_results(datadir, scores)

