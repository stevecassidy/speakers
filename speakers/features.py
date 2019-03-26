"""
Code to create feature servers in Sidekit

"""

import sidekit
import os
import numpy
import logging
from .config import config


def create_idmap(datadir, suffix):
    """Generate a map between basenames and speakers from
     a directory of audio data containing speaker directories
     return a Sidekit IdMap
    instance"""

    basenames = []
    speakers = []
    for dirpath, dirnames, filenames in os.walk(datadir):
        speaker = os.path.split(dirpath)[1]
        for fn in filenames:
            if fn.endswith(suffix):
                basename, ext = os.path.splitext(fn)
                speakers.append(speaker)
                basenames.append(basename)

    # make an idmap between speakers and basenames
    idmap = sidekit.IdMap()
    idmap.leftids = numpy.array(speakers)
    idmap.rightids = numpy.array(basenames)
    idmap.start = numpy.empty((len(speakers)), dtype="|O") # no start
    idmap.stop = numpy.empty(len(speakers), dtype="|O")    # no end

    return idmap


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
    channel_list = numpy.zeros_like(basenames, dtype = int)  # list of zeros one per basename
    # save features for all input files
    extractor.save_list(show_list=basenames,
                        audio_file_list=audio_filenames,
                        channel_list=channel_list,
                        num_thread=int(config('THREADS')))

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
                                    mask="[0-12]",
                                    feat_norm="cmvn",
                                    global_cmvn=None,
                                    dct_pca=False,
                                    dct_pca_config=None,
                                    sdc=False,
                                    sdc_config=None,
                                    delta=True,
                                    double_delta=True,
                                    delta_filter=None,
                                    context=None,
                                    traps_dct_nb=None,
                                    rasta=True,
                                    keep_all_features=True)

    return server


if __name__ == '__main__':
    create_idmap('data/ubm', 'wav')