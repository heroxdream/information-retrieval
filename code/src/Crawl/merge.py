__author__ = 'hanxuan'

from Utils.ues import es

from Utils.ucluster import cluster

from setup_cluster import DATA_SET as cluster_index

from setup_es_ import DATA_SET as es_index

# import pprint

import string

import mmh3

# es_index = 'aiw_test'

# result = es.search(
#     index=es_index,
#     body={
#         "size": 300000,
#         "fields": ["_id"],
#         "query": {
#             "match_all": {}
#         }
#     },
#     timeout=600
# )

# es_ids = xrange(0, 20000)
# for re in result['hits']['hits']:
#     # print re['_id']
#     es_ids.append(re['_id'])
#
# print 'es_ids get...'
es_ids = xrange(0, 20000)


duplicate = 0
def in_cluster(id_hash):
    global duplicate

    res = cluster.search(
        index=cluster_index,
        body={
            'query': {
                'filtered': {
                    'query': {
                        "match_all": {}
                    },
                    'filter': {
                        "ids": {
                            "values": [
                                id_hash
                            ]
                        }
                    }
                }
            },
            "fields": []
        }
    )

    if res['hits']['total'] == 1:
        duplicate += 1
        print '{} duplicates find.'.format(duplicate)
        return True
    else:
        # print res['hits']
        return False

counter = 0
for id in es_ids:
    result = es.search(
        index=es_index,
        body={
            'query': {
                'filtered': {
                    'query': {
                        "match_all": {}
                    },
                    'filter': {
                        "ids": {
                            "values": [
                                int(id)
                            ]
                        }
                    }
                }
            }
        }
    )
    source = result['hits']['hits'][0]['_source']

    url = string.strip(source['url'], '/')

    # print url

    id_hash = mmh3.hash(url)

    if in_cluster(id_hash): continue

    doc = dict(docno=url, html_Source=source['html'], HTTPheader=source['header'],author='xuan',
               text=source['text'], title=source['title'], out_links=source['out_links'])
    res = cluster.index(index=cluster_index, doc_type='document', id=id_hash, body=doc, timeout=60)
    if not res['created']:
        print 'insert error '

    counter += 1

    if counter % 100 == 0:
        print '{} entries processed...'.format(counter)

