__author__ = 'hanxuan'

from Utils.ulog import log

import numpy as np

def uniq_url(data_set, es):

    uniq_url_set = set()

    body={
        "fields": ['docno'],
        "query": {
            "match_all": {}
        }
    }

    resp = es.search(index=data_set, doc_type='document',body=body, explain=False, scroll="100m",size=1000)
    scroll_id = resp['_scroll_id']
    while True:
        for i in resp['hits']['hits']:
            url = i['fields']['docno'][0]
            uniq_url_set.add(url)
        resp = es.scroll(scroll_id=scroll_id, scroll='100m')
        if len(resp['hits']['hits']) > 0:
            log.info('finish scroll once')
            scroll_id = resp['_scroll_id']
        else:
            log.info('scrollId2: {}'.format(scroll_id))
            break

    return uniq_url_set


def write_to_file(id_docno_map, top_list, file_path):
    out_file = open(file_path, 'w')
    for tpl in top_list:
        out_file.write('{}\t{}\n'.format(id_docno_map[tpl[0]],tpl[1]))
    out_file.close()


def top_results(data_map, top_n):
    tpls = []
    sorted_tuple = sorted(data_map.items(), key=lambda x:x[1], reverse=True)
    for i in xrange(0, min(top_n, len(sorted_tuple))): tpls.append(sorted_tuple[i])
    return tpls

def kl(p, q):
    p = np.asarray(p) * 1.0 / np.sum(p)
    q = np.asarray(q) * 1.0 / np.sum(q)
    return sum(np.multiply(p, np.log2(p / q)))

def perplexity(p):
    p = np.asarray(p) * 1.0 / np.sum(p)
    return np.power(2, -sum(np.multiply(p, np.log2(p))))


# if __name__ == '__main__':
#     p = [1, 2, 3]
#     q = [1, 2, 3]
#
#     print perplexity(p)