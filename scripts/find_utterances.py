import speakers.log
from speakers.alveo_support import speakers_component
from speakers.config import configinit, config
import json
import sys

configinit('config.ini')

if __name__=='__main__':

    with open(config('UBM_SPEAKER_LIST')) as fd:
        speakers = [x.strip() for x in fd.readlines()]

    items = speakers_component(speakers, config('UBM_AUSTALK_COMPONENT'))

    with open(config('UBM_UTTERANCE_JSON'), 'w') as fd:
        json.dump(items, fd, indent=4)

    print("Wrote %d items to %s" % (len(items), config('UBM_UTTERANCE_JSON')))