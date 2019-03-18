"""
    Code to interact with Alveo to get data etc.

"""
import os
import pyalveo
import sidekit
import numpy
import logging
from .config import config
import csv


def read_speaker_csv(csvfile):
    """Read the speaker.csv file downloaded from austalk-query
    and return a dictionary with speaker ids as keys and a dict
    of properties as the value"""

    result = {}
    with open(csvfile) as fd:
        reader = csv.DictReader(fd)
        for row in reader:
            result[row['id']] = row

    return result


def get_alveo_data(item_list_url, directory):
    """Using the Alveo API get the audio data for the configured
    item list.
    Return a list of speaker identifiers and a list of file
    basenames that have been stored in DATA_DIR

    config: DATA_DIR, ALVEO_API_URL, ALVEO_API_KEY
    """

    client = pyalveo.Client(api_url=config("ALVEO_API_URL"), api_key=config("ALVEO_API_KEY"))
    item_list = client.get_item_list(item_list_url)

    # For each item we need to get the speaker identifier and the target audio file.
    item_meta = item_list.get_all()

    speakers = [i.metadata()['alveo:metadata']['olac:speaker'] for i in item_meta]

    data_dir = os.path.join(config("DATA_DIR"), directory)

    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    filepaths = []
    basenames = []
    for item in item_meta:
        docs = item.get_documents()
        for doc in docs:
            if doc.get_filename().endswith("speaker16.wav"):
                path = doc.download_content(dir_path=data_dir)
                filepaths.append(path)
                basenames.append(os.path.splitext(os.path.basename(doc.get_filename()))[0])
    logging.info("Downloaded %d files" % len(filepaths))

    return speakers, basenames


def speakers_component(speakers, component):
    """Generate a list of items for a given set of speakers
    containing all items from the given component (eg. digits, sentences)
    Return a list of item URLs"""

    client = pyalveo.Client(api_url=config("ALVEO_API_URL"), api_key=config("ALVEO_API_KEY"))

    query = """PREFIX dcterms:<http://purl.org/dc/terms/>
PREFIX foaf:<http://xmlns.com/foaf/0.1/>
PREFIX austalk:<http://ns.austalk.edu.au/>
PREFIX olac:<http://www.language-archives.org/OLAC/1.1/>
PREFIX ausnc:<http://ns.ausnc.org.au/schemas/ausnc_md_model/>

SELECT ?spkrid ?item ?prompt ?session ?audio WHERE {
	BIND ('%s' as ?spkrid)
    ?spkr a foaf:Person .
    ?spkr dcterms:identifier ?spkrid .
  	?item olac:speaker ?spkr .
    ?item austalk:componentName '%s' .
    ?item austalk:prototype ?prot .
    ?prot austalk:prompt ?prompt .
    ?item austalk:session ?session .
    ?item ausnc:document ?audio .
    ?audio austalk:channel 'ch6-speaker16' .
} 
    """
    items = []
    for spkr in speakers:
        qq = query % (spkr, component)

        result = client.sparql_query('austalk', qq)
        bindings = result['results']['bindings']

        print("speaker", spkr, " has ", len(bindings), "matches")
        for b in bindings:
            row = {
                'item': b['item']['value'],
                'spkrid': b['spkrid']['value'],
                'prompt': b['prompt']['value'],
                'session': b['session']['value'],
                'audio': b['audio']['value']
            }
            items.append(row)
    return items