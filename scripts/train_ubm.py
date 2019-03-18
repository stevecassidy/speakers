import speakers.log
from speakers.ubm import train_ubm
from speakers.features import make_feature_server, extract_features
from speakers.alveo_support import get_alveo_data
from speakers.config import configinit, config

configinit("config.ini")
speakers, basenames = get_alveo_data(config('UBM_ITEM_LIST_URL'), "ubm")

extract_features(basenames, "ubm", "ubm")
fs = make_feature_server("ubm")
train_ubm(fs, basenames)


