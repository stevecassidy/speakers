from speakers.config import configinit
from speakers.alveo_support import get_alveo_data, create_idmap
from speakers.features import make_feature_server
from speakers. train_ubm import load_or_train_ubm, sufficient_stats, adapt_models

configinit("config.ini")

speakers, basenames = get_alveo_data()

idmap = create_idmap(speakers, basenames)

featureserver = make_feature_server()

ubm = load_or_train_ubm(featureserver, basenames)

sufstat = sufficient_stats(idmap, featureserver, ubm)

speakermodels = adapt_models(ubm, sufstat)

