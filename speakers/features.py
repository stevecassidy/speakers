"""
Code to create feature servers in Sidekit

"""

import sidekit
import os
import numpy
import logging
from .config import config


def create_idmap(speakers, basenames):
    """Given a list of speakers and file basenames, return a Sidekit IdMap
    instance"""
    # make an idmap between speakers and filenames
    idmap = sidekit.IdMap()
    idmap.leftids = numpy.array(speakers)
    idmap.rightids = numpy.array(basenames)
    idmap.start = numpy.empty((len(speakers)), dtype="|O") # no start
    idmap.stop = numpy.empty(len(speakers), dtype="|O")    # no end

    idmap.validate()

    return idmap


def extract_features(basenames, data_dir, feat_dir):
    """
    Extract features from a set of data in data_dir (*.wav)
    and write features into feat_dir for future use
    """

    # TODO: more of these settings should be derived from the config file

    dd = os.path.join(config('DATA_DIR'), data_dir)
    fd = os.path.join(config('FEAT_DIR'), feat_dir)

    # clear the feature directory of old files
    if len(os.listdir(fd)) > 0:
        logging.info("Feature files already present...skipping")
        return

    logging.info("Extracting features for data in %s to %s" % (data_dir, feat_dir))

    # make a feature server to compute features over our audio files
    extractor = sidekit.FeaturesExtractor(audio_filename_structure=dd+'/{}.wav',
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

    channel_list = numpy.zeros_like(basenames, dtype = int)  # list of zeros one per basename
    # save features for all input files
    extractor.save_list(show_list=basenames, channel_list=channel_list, num_thread=int(config('THREADS')))

    logging.info("Features extracted")


def make_feature_server(feat_dir):
    """Return a Sidekit FeatureServer instance for this
    experiement
    """

    fd = os.path.join(config('FEAT_DIR'), feat_dir)

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