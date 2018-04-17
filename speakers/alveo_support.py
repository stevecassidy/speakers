"""
    Code to interact with Alveo to get data etc.

"""
import os
import pyalveo
import sidekit
import numpy
from .config import config


def get_alveo_data():
    """Using the Alveo API get the audio data for the configured
    item list.
    Return a list of speaker identifiers and a list of file
    basenames that have been stored in DATA_DIR

    config: ITEM_LIST_URL, DATA_DIR, ALVEO_API_URL, ALVEO_API_KEY
    """

    item_list_url = config("ITEM_LIST_URL")

    client = pyalveo.Client(api_url=config("ALVEO_API_URL"), api_key=config("ALVEO_API_KEY"))
    item_list = client.get_item_list(item_list_url)

    # For each item we need to get the speaker identifier and the target audio file.
    item_meta = item_list.get_all()

    speakers = [i.metadata()['alveo:metadata']['olac:speaker'] for i in item_meta]

    data_dir = config("DATA_DIR")

    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    filepaths = []
    basenames = []
    for item in item_meta:
        docs = item.get_documents()
        for doc in docs:
            if doc.get_filename().endswith("wav"):
                path = doc.download_content(dir_path="data")
                filepaths.append(path)
                basenames.append(os.path.splitext(os.path.basename(doc.get_filename()))[0])
    print("Downloaded", len(filepaths), "files")

    return speakers, basenames


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