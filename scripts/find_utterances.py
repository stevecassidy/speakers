import speakers.log
from speakers.alveo_support import speakers_component
from speakers.config import configinit, config
import json
import os

configinit('config.ini')


def find_utts(speaker_file, component, output_json):

    with open(speaker_file) as fd:
        speakers = [x.strip() for x in fd.readlines()]

    items = speakers_component(speakers, component)

    with open(os.path.join('data', output_json), 'w') as fd:
        json.dump(items, fd, indent=4)

    return items


if __name__ == '__main__':

    component = config('UBM_AUSTALK_COMPONENT')
    items = find_utts('ubm-speakers.txt', component, 'ubm-'+component+'.json')
    print("Wrote %d items to %s" % (len(items), 'ubm-'+component+'.json'))

    component = config('DEV_AUSTALK_COMPONENT')
    for spkrset in ['dev', 'test', 'eval']:
        items = find_utts(spkrset + '-speakers.txt', component, spkrset+'-'+component+'.json')
        print("Wrote %d items to %s" % (len(items), spkrset+'-'+component+'.json'))
