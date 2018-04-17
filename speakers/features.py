"""
Code to create feature servers in Sidekit

"""

import sidekit
from .config import config


def make_feature_server():
    """Return a Sidekit FeatureServer instance for this
    experiement

    config:  DATA_DIR, FEAT_DIR

    """
    dd = config('DATA_DIR')
    fd = config('FEAT_DIR')

    # TODO: more of these settings should be derived from the config file

    # make a feature server to compute features over our audio files
    extractor = sidekit.FeaturesExtractor(audio_filename_structure=dd+'{}.wav',
                                          feature_filename_structure=fd+"{}.h5",
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
                                          keep_all_features=True)

    server = sidekit.FeaturesServer(features_extractor=extractor,
                                    feature_filename_structure=fd+"{}.h5",
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