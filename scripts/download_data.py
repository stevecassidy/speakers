import speakers.log
from speakers.alveo_support import get_data_for_items
from speakers.config import configinit
import json
import sys

configinit('config.ini')

if __name__ == '__main__':

    with open(sys.argv[1]) as fd:
        items = json.load(fd)

    get_data_for_items(items, sys.argv[2])
