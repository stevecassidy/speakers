import speakers.log
from speakers.config import configinit, config
import os

configinit('config.ini')


def split_enrollment(datadir, suffix='wav', n=5):
    """Generate lists of enrollment and test data
    from a directory containing sub-directories per speaker

    datadir - the data directory
    suffix - file suffix to look for data files
    n - number of files to include in enrollment data

    Returns two lists (enrol, test) where each
    is a list of pairs (speaker, basename)
     """

    enrol = []
    test = []
    for dirpath, dirnames, filenames in os.walk(datadir):
        speaker = os.path.split(dirpath)[1]
        speaker_basenames = []
        for fn in filenames:
            if fn.endswith(suffix):
                basename, ext = os.path.splitext(fn)
                speaker_basenames.append((speaker, basename))

        # take the first basenames as enrollment, remainder as test
        # if there aren't enough enrolment files, ignore this speaker
        if n < len(speaker_basenames):
            enrol.extend(speaker_basenames[:n])
            test.extend(speaker_basenames[n:])

    return enrol, test


def write_file(data, dir, filename):

    with open(os.path.join(dir, filename), 'w') as fd:
        for line in data:
            fd.write('%s,%s\n' % line)


if __name__ == '__main__':

    import argparse

    parser = argparse.ArgumentParser(description='Download data from Alveo.')
    parser.add_argument('dir', type=str, nargs='+',
                        help='directory containing speaker data')
    parser.add_argument('--suffix', type=str, default='wav', help="file suffix to search for")
    parser.add_argument('--n', type=int, default=5, help='number of enrolment files per speaker')

    args = parser.parse_args()

    for dir in args.dir:
        enrol, test = split_enrollment(dir, suffix=args.suffix, n=args.n)
        write_file(enrol, dir, "enrol.csv")
        write_file(test, dir, "test.csv")

