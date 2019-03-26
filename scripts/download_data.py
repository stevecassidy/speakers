import speakers.log
from speakers.alveo_support import get_data_for_items
from speakers.config import configinit, config
import json
import os

configinit('config.ini')

if __name__ == '__main__':

    import argparse

    parser = argparse.ArgumentParser(description='Download data from Alveo.')
    parser.add_argument('json', type=str, nargs='+',
                        help='JSON file containing item descriptors')

    args = parser.parse_args()

    for jsonfile in args.json:
        with open(jsonfile) as fd:
            items = json.load(fd)

        # derive outdir from json filename
        outdir, ext = os.path.splitext(os.path.basename(jsonfile))
        get_data_for_items(items, outdir)
