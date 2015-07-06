__author__ = 'hanxuan'

from Algorithms.PageRank import PageRank

# from Utils.ucluster import cluster

from Utils.ues import es

from collections import defaultdict

from Utils.ulog import log

from Algorithms import util_methods

data_set = 'aiw_yi'

docno_id_map = dict()
id_docno_map = dict()

def uniq_ids():

    id_counter = 0

    body={
        "fields": ['url'],
        "query": {
            "match_all": {}
        }
    }

    resp = es.search(index=data_set, doc_type='document',body=body, explain=False, scroll="100m",size=2000)

    scrollId = resp['_scroll_id']

    while True:
        for i in resp['hits']['hits']:
            url = i['fields']['url'][0]
            docno_id_map[url] = id_counter
            id_docno_map[id_counter] = url
            id_counter += 1

        resp = es.scroll(scroll_id=scrollId, scroll='100m')
        if len(resp['hits']['hits']) > 0:
            log.info('finish scroll once')
            scrollId = resp['_scroll_id']
        else:
            log.info('scrollId2: {}'.format(scrollId))
            break

    log.info('uniq_urls: {} {} {}'.format(len(docno_id_map), len(id_docno_map), id_counter))

def build_adjacent_list():

    adjacent_list = defaultdict(list)

    body = {
        "fields": ['out_links', 'url'],
        "query": {
            "match_all": {}
        }
    }

    resp = es.search(index=data_set, doc_type='document',body=body, explain=False, scroll="100m", size=2000)
    scrollId = resp['_scroll_id']
    while True:
        for i in resp['hits']['hits']:

            url = i['fields']['url'][0]

            url_id = docno_id_map[url]

            adjacent_list[url_id] = []

            if 'out_links' not in i['fields']: continue

            for link in i['fields']['out_links']:
                if link in docno_id_map: adjacent_list[url_id].append(docno_id_map[link])

        resp = es.scroll(scroll_id = scrollId, scroll='100m')
        if len(resp['hits']['hits']) > 0:
            log.info('finish scroll once')
            scrollId = resp['_scroll_id']
        else:
            log.info('scrollId2: {}'.format(scrollId))
            break

    log.info('adj_list size {}'.format(len(adjacent_list)))

    return adjacent_list


def run():
    uniq_ids()

    log.info('uniq_urls finished')

    aj_list = build_adjacent_list()

    log.info('aj_list finished')

    pr = PageRank(aj_list)
    pr.loop()
    top_500 = pr.top_results(500)

    craw_pr_file = 'results/pagerank.crawl.500.txt'
    util_methods.write_to_file(id_docno_map, top_500, craw_pr_file)

if __name__ == '__main__':
    run()
