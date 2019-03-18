from speakers.alveo_support import read_speaker_csv

if __name__=='__main__':

    import sys
    import random
    random.seed(200)  # fixed seed for reproducible results

    speakers = read_speaker_csv(sys.argv[1])

    males = [spk for spk in speakers.keys() if speakers[spk]['gender'] == 'male']
    females = [spk for spk in speakers.keys() if speakers[spk]['gender'] == 'female']

    print(len(males), len(females))

    ubm_proportion = 0.4
    ubm_males = random.sample(males, int(len(males)*ubm_proportion))
    ubm_females = random.sample(females, int(len(females)*ubm_proportion))

    ubm_speakers = []
    ubm_speakers.extend(ubm_males)
    ubm_speakers.extend(ubm_females)
    ubm_speakers.sort()

    remaining = []
    for spkr in speakers.keys():
        if spkr not in ubm_speakers:
            remaining.append(spkr)

    with open('ubm-speakers.txt', 'w') as fd:
        for spkr in ubm_speakers:
            fd.write(spkr + '\n')

    with open('remaining-speakers.txt', 'w') as fd:
        for spkr in remaining:
            fd.write(spkr + '\n')

    print(len(ubm_males), len(ubm_females))
    print(ubm_males[:3])
    print(ubm_females[:3])

    ages_m = [int(speakers[spk]['age']) for spk in ubm_males]
    ages_f = [int(speakers[spk]['age']) for spk in ubm_females]

    ages_all = [int(speakers[spk]['age']) for spk in speakers.keys()]

    print(sum(ages_m)/len(ages_m))
    print(sum(ages_f)/len(ages_f))
    print(sum(ages_all)/len(ages_all))