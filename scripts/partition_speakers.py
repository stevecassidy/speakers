from speakers.alveo_support import speakers_with_data, read_speaker_csv
from speakers.config import configinit, config_bool
import os

if __name__=='__main__':

    import sys
    import random
    random.seed(200)  # fixed seed for reproducible results
    configinit('config.ini')

    speakers = read_speaker_csv(sys.argv[1])
    speakers_d = speakers_with_data()

    males = [spk for spk in speakers.keys() if speakers[spk]['gender'] == 'male' and spk in speakers_d]
    females = [spk for spk in speakers.keys() if speakers[spk]['gender'] == 'female' and spk in speakers_d]

    # shuffle the speakers so we can select dev, eval and test sets
    random.shuffle(males)
    random.shuffle(females)

    # select 100 speakers per set, balanced m/f
    data = {
        'dev': {'male': males[:50], 'female': females[:50]},
        'test': {'male': males[50:100], 'female':females[50:100]},
        'eval' : {'male':males[100:150], 'female':females[100:150]},
        'ubm': {'male':males[150:], 'female':females[150:]},   # ubm speakers are all remaining
    }

    if not os.path.exists('data'):
        os.makedirs('data')

    genders = ['male', 'female']

    for key in data.keys():
        for gender in genders:
            outfile = os.path.join('data', key+'-'+gender+'-speakers.txt')
            with open(outfile, 'w') as fd:
                for spkr in data[key][gender]:
                    fd.write(spkr + '\n')

