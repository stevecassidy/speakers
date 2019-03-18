import datetime
import logging
import os
from speakers.config import config, configinit, items

configinit("config.ini")

logfile = os.path.join('log', 'experiment-%s.log' % datetime.datetime.ctime(datetime.datetime.now()))
logging.basicConfig(filename=logfile, level=logging.INFO)

logging.info("Experiment config")
for key, value in items():
    logging.info("\t%s:\t%s" % (key, value))