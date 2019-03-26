import speakers.log
from speakers.ubm import train_ubm
from speakers.config import configinit, config

configinit("config.ini")

train_ubm()


