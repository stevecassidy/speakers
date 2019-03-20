import speakers.log
from speakers.alveo_support import get_data_for_items
from speakers.config import configinit, config
import json

configinit('config.ini')

if __name__ == '__main__':

    with open(config('UBM_UTTERANCE_JSON')) as fd:
        items = json.load(fd)

    get_data_for_items(items, config('UBM_DATA_DIR'))
