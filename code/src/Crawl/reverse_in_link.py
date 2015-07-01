__author__ = 'hanxuan'

from Utils.ucluster import cluster

from setup_cluster import DATA_SET as cluster_index

import string

from collections import defaultdict

uniq_urls = set()

body={
    "fields": ['docno'],
    "query": {
        "match_all": {}
    }
}

resp = cluster.search(index=cluster_index, doc_type='document',body=body, explain=False, scroll="100m",size=100)

scrollId = resp['_scroll_id']

while True:
    if resp is None:
        print "resp none"
        break
    for i in resp['hits']['hits']:
        uniq_urls.add(i['fields']['docno'][0])
    resp = cluster.scroll(scroll_id = scrollId, scroll='100000ms')
    if len(resp['hits']['hits']) > 0:
        scrollId = resp['_scroll_id']
    else:
        print 'scrollId1: {}'.format(scrollId)
        break

print 'uniq_urls: {}'.format(len(uniq_urls))




body = {
    "fields": ['out_links', 'docno'],
    "query": {
        "match_all": {}
    }
}

in_link_map = defaultdict(set)

resp = cluster.search(index=cluster_index, doc_type='document',body=body, explain=False, scroll="100m",size=100)
scrollId = resp['_scroll_id']
counter = 0
while True:

    if resp is None:
        print "resp none"
        break

    for i in resp['hits']['hits']:

        url = i['fields']['docno'][0]
        out_links_this = set()

        if 'out_links' not in i['fields']: continue

        for link in i['fields']['out_links']:
            out_links_this.add(string.strip(link, '/'))

        intersection = out_links_this.intersection(uniq_urls)

        for link in intersection:
            in_link_map[link].add(url)

    resp = cluster.scroll(scroll_id = scrollId, scroll='100000ms')
    if len(resp['hits']['hits']) > 0:
        scrollId = resp['_scroll_id']
    else:
        print 'scrollId2: {}'.format(scrollId)
        break

    counter += 100
    if counter % 1000 == 0:
        print '{} entries processed...'.format(counter)

print 'out_link_map: {}'.format(len(in_link_map))

import mmh3
counter = 0
for link in in_link_map:
    id = mmh3.hash(link)
    cluster.update(index=cluster_index, doc_type='document', id=id, body={'doc':{'in_links':list(in_link_map[link])}}, timeout=60)

    counter += 1
    if counter % 100 == 0:
        print '{} updated...'.format(counter)

print 'success'