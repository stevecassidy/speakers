"""
    Code to interact with Alveo to get data etc.

"""
import os
import pyalveo
import logging
from .config import config
import csv
from random import sample


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


def speakers_with_data(component='digits'):
    """Query the Alveo API to find speakers with at least some data for a given
    component"""

    client = pyalveo.Client(api_url=config("ALVEO_API_URL"), api_key=config("ALVEO_API_KEY"))

    qq = """
PREFIX dcterms:<http://purl.org/dc/terms/>
PREFIX foaf:<http://xmlns.com/foaf/0.1/>
PREFIX austalk:<http://ns.austalk.edu.au/>
PREFIX olac:<http://www.language-archives.org/OLAC/1.1/>
PREFIX ausnc:<http://ns.ausnc.org.au/schemas/ausnc_md_model/>

SELECT ?spkrid (count(?item) as ?itemcount) WHERE {
    ?item olac:speaker ?spkr .
    ?spkr dcterms:identifier ?spkrid .
    ?item austalk:componentName '%s' .
    ?item austalk:session ?session .
} group by ?spkrid  
""" % component

    result = client.sparql_query('austalk', qq)
    bindings = result['results']['bindings']

    speakers = []
    for b in bindings:
        if int(b['itemcount']['value']) > 0:
            speakers.append(b['spkrid']['value'])

    return speakers


def get_alveo_data(item_list_url, directory):
    """Using the Alveo API get the audio data for the configured
    item list.
    Return a list of speaker identifiers and a list of file
    basenames that have been stored in DATA_DIR

    config: DATA_DIR, ALVEO_API_URL, ALVEO_API_KEY
    """

    client = pyalveo.Client(api_url=config("ALVEO_API_URL"), api_key=config("ALVEO_API_KEY"), use_cache=False, update_cache=False)
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
                try:
                    path = os.path.join(data_dir, doc.get_filename())
                    if not os.path.exists(path):
                        print(path)
                        path = doc.download_content(dir_path=data_dir)
                        print(".", flush=True, end='')
                    else:
                        print("|", flush=True, end='')
                    filepaths.append(path)
                    basenames.append(os.path.splitext(os.path.basename(doc.get_filename()))[0])
                except pyalveo.pyalveo.APIError:
                    print("^", flush=True, end='')

    logging.info("Downloaded %d files" % len(filepaths))

    return speakers, basenames


def get_data_for_items(items, directory):
    """Get data for a list of items with audio URLs

    Return a list of speaker identifiers and a list of file
    basenames that have been stored in DATA_DIR

    config: DATA_DIR, ALVEO_API_URL, ALVEO_API_KEY
    """

    client = pyalveo.Client(api_url=config("ALVEO_API_URL"), api_key=config("ALVEO_API_KEY"), use_cache=False, update_cache=False)

    data_dir = os.path.join(config("DATA_DIR"), directory)

    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    basenames = []
    for item in items:
        doc = pyalveo.Document({'alveo:url': item['audio']}, client)
        dir = os.path.join(data_dir, item['spkrid'])
        if not os.path.exists(dir):
            os.makedirs(dir)

        try:
            path = os.path.join(dir, doc.get_filename())
            if not os.path.exists(path):
                path = doc.download_content(dir_path=dir)
                print(".", flush=True, end='')
            else:
                print("|", flush=True, end='')

            basenames.append(os.path.splitext(os.path.basename(doc.get_filename()))[0])
        except:
            print("^", flush=True, end='')

    logging.info("Downloaded %d files" % len(basenames))

    return basenames


def speakers_component(speakers, component, count=None, random=False):
    """Generate a list of items for a given set of speakers
    containing all items from the given component (eg. digits, sentences)

    If n is not None it is an integer and only n items per speaker are retrieved.

    If random=True, n items are selected at random, otherwise the first n items
    per speaker are selected.

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
    with open('problem-speakers.txt', 'w') as fd:
        fd.write('speakers_component for ' + component)

    items = []
    for spkr in speakers:
        speaker_items = []
        qq = query % (spkr, component)

        try:
            result = client.sparql_query('austalk', qq)
            bindings = result['results']['bindings']

            print('%d.' % len(bindings), end='', flush=True)
            for b in bindings:
                row = {
                    'item': b['item']['value'],
                    'spkrid': b['spkrid']['value'],
                    'prompt': b['prompt']['value'],
                    'session': b['session']['value'],
                    'audio': b['audio']['value']
                }
                speaker_items.append(row)
        except:
            print("Problem with query for ", spkr)
            with open('problem-speakers.txt', 'a') as fd:
                fd.write(spkr)
                fd.write('\n')

        if count:
            if random and (count <= len(speaker_items)):
                speaker_items = sample(speaker_items, count)
            else:
                speaker_items = speaker_items[:count]
        items += speaker_items

    return items



if __name__ == '__main__':

    from .config import configinit

    configinit('config.ini')

    print(speakers_with_data('digits'))