import speakers.log
from speakers.ubm import train_ubm
from speakers.features import make_feature_server, extract_features
from speakers.alveo_support import get_alveo_data
from speakers.config import configinit, config

configinit("config.ini")

train_ubm()


