"""
Code to create feature servers in Sidekit

"""

import sidekit
import os
import numpy
import logging
from .config import config, config_bool, config_int


def read_speaker_csv(filename):
    """Read data from a csv file with speaker, basename pairs

    return two lists: speakers, basenames
    """

    speakers = []
    basenames = []
    with open(filename) as fd:
        for line in fd:
            line = line.strip()
            speaker, basename = line.split(',')
            speakers.append(speaker)
            basenames.append(basename)

    return speakers, basenames


def create_idmap(filename):
    """Generate a map between basenames and speakers from
    a csv file

    return a Sidekit IdMap instance
     """

    speakers, basenames = read_speaker_csv(filename)

    idmap = sidekit.IdMap()
    idmap.leftids = numpy.array(speakers)
    idmap.rightids = numpy.array(basenames)
    idmap.start = numpy.empty((len(speakers)), dtype="|O") # no start
    idmap.stop = numpy.empty(len(speakers), dtype="|O")    # no end

    return idmap


def create_key(csvfile):
    """Define target and non target trials"""

    # define the target and non target (imposter) trials
    # for each speaker we have a vector of booleans that say whether
    # each segment is a target or not

    speakers, basenames = read_speaker_csv(csvfile)

    key = sidekit.Key()
    # models and segments are the same as defined in the training data
    unique_speakers = list(set(speakers))
    key.modelset = numpy.array(unique_speakers)
    key.segset = numpy.array(basenames)

    key.tar = numpy.zeros((key.modelset.size, key.segset.size), dtype='bool')

    key.tar[0,0] = False
    key.non = numpy.zeros((key.modelset.size, key.segset.size), dtype='bool')
    key.non[0,0] = True

    trows = []
    nrows = []
    for sp in key.modelset:
        tar = numpy.array(speakers) == sp
        non = numpy.array(speakers) != sp
        trows.append(tar)
        nrows.append(non)

    key.tar = numpy.array(trows)
    key.non = numpy.array(nrows)

    return key


def create_ndx(filename):

    # the ndx object stores the testing trials to be evaluated and the models to be used
    speakers, basenames = read_speaker_csv(filename)

    unique_speakers = list(set(speakers))
    ndx = sidekit.Ndx()
    ndx.modelset = numpy.array(unique_speakers)  # list of distinct models
    ndx.segset = numpy.array(basenames)        # list of trial segments to be tested
    ndx.trialmask = numpy.ones((len(unique_speakers), len(basenames)), dtype='bool')

    return ndx


def find_basenames(datadir, suffix):
    """Return a list of file basenames ending in suffix in the given directory
    and below (recursive)"""

    basenames = []
    audio_filenames = []
    for dirpath, dirnames, filenames in os.walk(datadir):
        for fn in filenames:
            if fn.endswith(suffix):
                basename, ext = os.path.splitext(fn)
                audio_filenames.append(os.path.join(dirpath, fn))
                basenames.append(basename)

    return basenames, audio_filenames


def extract_features(dirname):
    """
    Extract features from a set of data in DATA_DIR/dirname (*.wav)
    and write features into FEAT_DIR/dirname for future use
    """

    # TODO: more of these settings should be derived from the config file

    dd = os.path.join(config('DATA_DIR'), dirname)
    fd = os.path.join(config('FEAT_DIR'), dirname)

    if not os.path.exists(fd):
        os.makedirs(fd)

    # clear the feature directory of old files
    if len(os.listdir(fd)) > 0:
        logging.info("Feature files already present...skipping")
        return

    logging.info("Extracting features for data in %s to %s" % (dd, fd))

    # make a feature server to compute features over our audio files
    extractor = sidekit.FeaturesExtractor(audio_filename_structure=None,
                                          feature_filename_structure=fd+"/{}.h5",
                                          sampling_frequency=None,
                                          lower_frequency=200,
                                          higher_frequency=3800,
                                          filter_bank="log",
                                          filter_bank_size=24,
                                          window_size=0.025,
                                          shift=0.01,
                                          ceps_number=20,
                                          vad="snr",
                                          snr=40,
                                          pre_emphasis=0.97,
                                          save_param=["vad", "energy", "cep", "fb"],
                                          keep_all_features=False)

    basenames, audio_filenames = find_basenames(dd, 'wav')
    print(basenames)
    channel_list = numpy.zeros_like(basenames, dtype = int)  # list of zeros one per basename
    # save features for all input files
    extractor.save_list(show_list=basenames,
                        audio_file_list=audio_filenames,
                        channel_list=channel_list,
                        num_thread=config_int('THREADS', 1))

    logging.info("Features extracted")


def make_feature_server(dirname):
    """Return a Sidekit FeatureServer instance for this
    experiement
    """

    fd = os.path.join(config('FEAT_DIR'), dirname)

    server = sidekit.FeaturesServer(features_extractor=None,
                                    feature_filename_structure=fd+"/{}.h5",
                                    sources=None,
                                    dataset_list=["energy", "cep", "vad"],
                                    mask=config("FEATURE_MASK", None),
                                    feat_norm=config("FEATURE_NORMALISATION", "cmvn"),
                                    global_cmvn=None,
                                    dct_pca=False,
                                    dct_pca_config=None,
                                    sdc=False,
                                    sdc_config=None,
                                    delta=config_bool("FEATURES_DELTA", True),
                                    double_delta=config_bool("FEATURES_DOUBLE_DELTA", True),
                                    delta_filter=None,
                                    context=None,
                                    traps_dct_nb=None,
                                    rasta=config_bool("FEATURES_RASTA", True),
                                    keep_all_features=True)

    return server


if __name__ == '__main__':
    enrol, test = split_enrolment_data('data/ubm', 'wav', 5)

    for pair in enrol:
        print(pair)
    print('----------------------------')
    for pair in test:
        print(pair)