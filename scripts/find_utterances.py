import speakers.log
from speakers.alveo_support import speakers_component
from speakers.config import configinit, config
import json
import os

configinit('config.ini')


def find_utts(group, component, n, random=False):

    for gender in ['male', 'female']:
        speaker_file = os.path.join('data', group+'-'+gender+'-speakers.txt')
        output_file = os.path.join('data', group+'-'+gender+'-'+component+'.json')

        with open(speaker_file) as fd:
            speakers = [x.strip() for x in fd.readlines()]

        items = speakers_component(speakers, component, n, random=random)

        with open(output_file, 'w') as fd:
            json.dump(items, fd, indent=4)

        print("Wrote %d items to %s" % (len(items), output_file))


if __name__ == '__main__':

    component = config('UBM_AUSTALK_COMPONENT')
    n = int(config('UBM_AUSTALK_ITEMS_PER_SPEAKER'))
    random = config('UBM_AUSTALK_RANDOM_ITEMS') == 'True'
    find_utts('ubm', component, n, random)

    component = config('DEV_AUSTALK_COMPONENT')
    random = config('DEV_AUSTALK_RANDOM_ITEMS') == 'True'
    n = int(config('DEV_AUSTALK_ITEMS_PER_SPEAKER'))
    for spkrset in ['dev', 'test', 'eval']:
        find_utts(spkrset, component, n, random)
