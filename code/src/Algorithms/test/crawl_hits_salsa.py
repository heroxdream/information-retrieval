__author__ = 'hanxuan'

from Algorithms.HITS import HITS

from Algorithms.SALSA import SALSA

# from Utils.ucluster import cluster

from Utils.ues import es

from collections import defaultdict

from Utils.ulog import log

from Algorithms import util_methods


data_set = 'aiw_yi'
query = 'american independent war'

docno_id_map = dict()
id_docno_map = dict()
def generate_base_set(uniq_url_set):

    id_counter = 0

    body = {
        "size": 1000,
        "fields": ['url'],
        "query": {
            "match": {
                "text": query
            }
        }
    }

    resp = es.search(index=data_set, doc_type='document',body=body, explain=False)

    root_ids = set()

    for entry in resp['hits']['hits']:
        url = entry['fields']['url'][0]
        root_ids.add(entry['_id'])
        id_counter = put_to_maps(id_counter, url)

    for id_this in root_ids:
        body = {
            'query': {
                'filtered': {
                    'query': {
                        "match_all": {}
                    },
                    'filter': {
                        "ids": {
                            "values": [
                                id_this
                            ]
                        }
                    }
                }
            },
            "fields": ["out_links"]
        }
        resp = es.search(index=data_set, doc_type='document',body=body, explain=False)
        try:
            for entry in resp['hits']['hits'][0]['fields']['out_links']:
                if entry in uniq_url_set and entry not in docno_id_map: id_counter = put_to_maps(id_counter, entry)
        except Exception, e:
            log.info('EMPTY out_links for {} {}'.format(id_this, e))

    print len(docno_id_map)


out_link_map = defaultdict(list)
in_link_map = defaultdict(list)
def generate_out_in_links():

    body = {
        "fields": ['out_links', 'url'],
        "query": {
            "match_all": {}
        }
    }

    resp = es.search(index=data_set, doc_type='document',body=body, explain=False, scroll="100m", size=2000)
    scroll_id = resp['_scroll_id']
    while True:
        for i in resp['hits']['hits']:

            url = i['fields']['url'][0]

            if url not in docno_id_map: continue

            url_id = docno_id_map[url]

            out_link_map[url_id] = []
            if url_id not in in_link_map: in_link_map[url_id] = []

            if 'out_links' not in i['fields']: continue

            for link in i['fields']['out_links']:
                if link in docno_id_map:
                    out_link_map[url_id].append(docno_id_map[link])
                    in_link_map[docno_id_map[link]].append(url_id)

        resp = es.scroll(scroll_id = scroll_id, scroll='100m')
        if len(resp['hits']['hits']) > 0:
            log.info('finish scroll once')
            scroll_id = resp['_scroll_id']
        else:
            log.info('scrollId2: {}'.format(scroll_id))
            break

    log.info('out_link_map size {}'.format(len(out_link_map)))
    log.info('in_link_map size {}'.format(len(in_link_map)))


def put_to_maps(id_counter, url):
    docno_id_map[url] = id_counter
    id_docno_map[id_counter] = url
    id_counter += 1
    return id_counter


def prepare():
    uniq_url_set = util_methods.uniq_url(data_set, es)
    generate_base_set(uniq_url_set)
    generate_out_in_links()

def run_hits():
    hits = HITS(out_link_map, in_link_map)
    hits.loop()
    top_hub_500 = hits.top_hub(500)
    top_aut_500 = hits.top_authority(500)

    hit_hub_file = 'results/hits.hub.500.txt'
    util_methods.write_to_file(id_docno_map, top_hub_500, hit_hub_file)

    hit_authority_file = 'results/hits.authority.500.txt'
    util_methods.write_to_file(id_docno_map, top_aut_500, hit_authority_file)

def run_salsa():

    salsa = SALSA(out_link_map, in_link_map)
    salsa.loop()
    top_hub_500 = salsa.top_hub(500)
    top_aut_500 = salsa.top_authority(500)

    salsa_hub_file = 'results/salsa.hub.500.txt'
    util_methods.write_to_file(id_docno_map, top_hub_500, salsa_hub_file)

    salsa_authority_file = 'results/salsa.authority.500.txt'
    util_methods.write_to_file(id_docno_map, top_aut_500, salsa_authority_file)

if __name__ == '__main__':
    prepare()
    run_hits()
    run_salsa()