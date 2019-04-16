"""
    Code to train a Universal Background Model
"""
import logging
import os
import sidekit
import matplotlib.pyplot as plt
from .config import config, config_int, config_bool, config_float
from .features import make_feature_server, find_basenames, create_idmap, create_key, create_ndx


def ubmfile(gender):
    """Return the name for the ubm file for this configuration

    config: MODEL_DIR, NUMBER_OF_MIXTURES
    """

    ubmfile = 'ubm_{}_{}_{}.h5'.format(gender, config("NUMBER_OF_MIXTURES"), config("FEATURE_SIZE"))
    return os.path.join(config("MODEL_DIR"), ubmfile)


def train_ubm():
    """Train a UBM given the configuration settings
    Trains separate ubm models for each gender

    config: NUMBER_OF_MIXTURES, THREADS, SAVE_PARTIAL, MODEL_DIR
    """

    logging.info("Starting UBM Training")

    for gender in ['male', 'female']:

        datadir = "ubm-"+gender+"-"+config("UBM_AUSTALK_COMPONENT")

        fd = os.path.join(config('FEAT_DIR'), datadir)

        server = make_feature_server(datadir)

        basenames, feature_filenames = find_basenames(fd, 'h5')

        ubm = sidekit.Mixture()

        ubm.EM_split(features_server=server,
                     feature_list=basenames,
                     distrib_nb=int(config("NUMBER_OF_MIXTURES")),
                     num_thread=int(config("THREADS")),
                     ceil_cov=10,
                     floor_cov=1e-2
                     )

        # write out a copy of the trained UBM
        ubm.write(ubmfile(gender))
        logging.info("UBM model written to %s" % ubmfile(gender))


def load_ubm(gender):
    """Load a UBM from disk and return"""

    uf = ubmfile(gender)
    if os.path.exists(uf):
        ubm = sidekit.Mixture()
        ubm.read(uf)
        return ubm
    else:
        return None


def sufficient_stats(ubm, idmap, datadir):
    """
    Generate the sufficient statistics for speaker data given a UBM

    ubm - a trained UBM
    idmap - an idmap for the enrolment data
    datadir - name of subdirectory of FEAT_DIR containing training data

    config: NUMBER_OF_MIXTURES, THREADS, FEATURE_SIZE
    :return:
    """

    filename = os.path.join(config('MODEL_DIR'),
                            "sufstat_%s_%s_%s.h5" %
                            (datadir, config_int("NUMBER_OF_MIXTURES"), ubm.dim()))

    if os.path.exists(filename):
        print("Reading sufficient statistics from file", filename)
        sufstat = sidekit.StatServer(filename)
    else:
        server = make_feature_server(datadir)

        sufstat = sidekit.StatServer(idmap,
                                     distrib_nb=config_int('NUMBER_OF_MIXTURES'),
                                     feature_size=ubm.dim())
        sufstat.accumulate_stat(ubm=ubm,
                                feature_server=server,
                                seg_indices=range(sufstat.segset.shape[0]),
                                num_thread=config_int('THREADS'))
        sufstat.write(filename)

    return sufstat


def adapt_models(ubm, sufstat, datadir):
    """
    Adapt a UBM to a number of speakers via MAP adaptation

    config: MODEL_DIR
    :return:
    """

    regulation_factor = 3
    speaker_models = sufstat.adapt_mean_map_multisession(ubm, regulation_factor)

    filename = "speakers_%s_%s_%s.h5" % (datadir, config_int("NUMBER_OF_MIXTURES"), ubm.dim())
    speaker_models.write(os.path.join(config('MODEL_DIR'), filename))

    return speaker_models


def evaluate_models(ubm, speaker_models, datadir):
    """Evaluate speaker models on test data from
    datadir"""

    server = make_feature_server(datadir)

    test_csv = os.path.join("data", datadir, 'test.csv')
    test_ndx = create_ndx(test_csv)

    scores = sidekit.gmm_scoring(ubm,
                                 speaker_models,
                                 test_ndx,
                                 server,
                                 num_thread=config_int("THREADS"))

    filename = "scores_%s_%s_%s.h5" % (datadir, config_int("NUMBER_OF_MIXTURES"), ubm.dim())
    scores.write(os.path.join(config("MODEL_DIR"), filename))

    return scores


def plot_results(datadir, scores):
    """Generate a plot of results"""

    test_csv = os.path.join("data", datadir, 'test.csv')

    key = create_key(test_csv)
    plt.rcParams["figure.figsize"] = (10,10)
    prior = sidekit.effective_prior(0.01, 1, 1)

    dp = sidekit.DetPlot(window_style='sre10', plot_title='GMM-UBM')
    dp.set_system_from_scores(scores, key, sys_name='GMM-UBM')
    dp.create_figure()
    dp.plot_rocch_det(0)
    dp.plot_DR30_both(idx=0)
    dp.plot_mindcf_point(prior, idx=0)

    filename = "results_%s.pdf" % (datadir,)

    plt.savefig(filename)

    prior = sidekit.logit_effective_prior(0.01, 1, 1)
    minDCF, Pmiss, Pfa, prbep, eer = sidekit.bosaris.detplot.fast_minDCF(dp.__tar__[0], dp.__non__[0], prior, normalize=True)
    print("UBM-GMM, minDCF = {}, eer = {}, Pmiss = {}, Pfa = {}".format(minDCF, eer, Pmiss, Pfa))


if __name__=='__main__':

    from .config import configinit
    configinit('config.ini')

    import sys
    scores = sidekit.bosaris.Scores("scores.h5")
    datadir = sys.argv[1]
    plot_results(datadir, scores)