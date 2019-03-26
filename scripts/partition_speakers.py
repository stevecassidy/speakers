from speakers.alveo_support import read_speaker_csv
import os

def report(name, slist):

    print("Report for", name)

    males = [spk for spk in slist if speakers[spk]['gender'] == 'male']
    females = [spk for spk in slist if speakers[spk]['gender'] == 'female']

    print("M/F:", len(males), len(females))

    ages_m = [int(speakers[spk]['age']) for spk in males]
    ages_f = [int(speakers[spk]['age']) for spk in females]

    ages_all = [int(speakers[spk]['age']) for spk in slist]

    print("Average Male age:", sum(ages_m)/len(ages_m))
    print("Average Female age:", sum(ages_f)/len(ages_f))
    print("Overall average age:", sum(ages_all)/len(ages_all))

if __name__=='__main__':

    import sys
    import random
    random.seed(200)  # fixed seed for reproducible results

    speakers = read_speaker_csv(sys.argv[1])

    males = [spk for spk in speakers.keys() if speakers[spk]['gender'] == 'male']
    females = [spk for spk in speakers.keys() if speakers[spk]['gender'] == 'female']

    ubm_proportion = 0.4
    ubm_males = random.sample(males, int(len(males)*ubm_proportion))
    ubm_females = random.sample(females, int(len(females)*ubm_proportion))

    ubm_speakers = ubm_males + ubm_females
    ubm_speakers.sort()

    remaining_m = [s for s in males if s not in ubm_speakers]
    remaining_f = [s for s in females if s not in ubm_speakers]

    # shuffle the remainder so we can select dev, eval and test sets
    random.shuffle(remaining_m)
    random.shuffle(remaining_f)

    dev = remaining_m[:50] + remaining_f[:50]
    test = remaining_m[50:100] + remaining_f[50:100]
    eval = remaining_m[100:150] + remaining_f[100:150]

    dev.sort()
    test.sort()
    eval.sort()

    if not os.path.exists('data'):
        os.makedirs('data')

    with open('data/ubm-speakers.txt', 'w') as fd:
        for spkr in ubm_speakers:
            fd.write(spkr + '\n')

    with open('data/dev-speakers.txt', 'w') as fd:
        for spkr in dev:
            fd.write(spkr + '\n')

    with open('data/test-speakers.txt', 'w') as fd:
        for spkr in test:
            fd.write(spkr + '\n')
    with open('data/eval-speakers.txt', 'w') as fd:
        for spkr in eval:
            fd.write(spkr + '\n')

    report("UBM", ubm_speakers)
    report("DEV", dev)
    report("TEST", test)
    report("EVAL", eval)
