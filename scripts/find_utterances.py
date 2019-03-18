from speakers.alveo_support import speakers_component
from speakers.config import configinit
import json
import sys

configinit('config.ini')

if __name__=='__main__':

    with open(sys.argv[1]) as fd:
        speakers = [x.strip() for x in fd.readlines()]

    items = speakers_component(speakers, sys.argv[2])

    with open(sys.argv[3], 'w') as fd:
        json.dump(items, fd, indent=4)