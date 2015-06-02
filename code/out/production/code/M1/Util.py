__author__ = 'Xuan Han'

import string


from Constants import DATA_SET

from ES import es

from LOG import log


def strip_dot(term):
    term = string.rstrip(term)
    term = string.rstrip(term, '.')
    return term


def strip_punctuation(term):
    term = string.replace(term, ',', '')
    term = string.replace(term, '"', '')
    term = string.replace(term, '(', '')
    term = string.replace(term, ')', '')
    return term

def normalize_dict(d):
    factor = 1.0 / sum(d.itervalues())
    for k in d:
        d[k] *= factor
    return d


def get_docno(doc_id):
    result = es.search(
        index=DATA_SET,
        body={
            'query': {
                'filtered': {
                    'query': {
                        "match_all": {}
                    },
                    'filter': {
                        "ids": {
                            "values": [
                                int(doc_id)
                            ]
                        }
                    }
                }
            },
            "fields": ["docno"]
        }
    )
    return str(result['hits']['hits'][0]['fields']['docno'][0])

def get_all_tf_by_docid(docid):
    terms_tf = dict()
    result_tv = es.termvector(
        index=DATA_SET,
        doc_type='document',
        id=docid,
        fields=['text'],
        body={
            "offsets": False,
            "payloads": False,
            "positions": False,
            "term_statistics": False,
            "field_statistics": False
        }
    )

    if len(result_tv['term_vectors']) == 0:
        log.info('empty article found for %s', docid)
    else:
        terms_stats = result_tv['term_vectors']['text']['terms']
        for term in terms_stats:
            terms_tf[str(term)] = terms_stats[term]['term_freq']

    return terms_tf


def bigram_distance(docid, w1, w2):

    result_tv = es.termvector(
        index=DATA_SET,
        doc_type='document',
        id=docid,
        fields=['text'],
        body={
            "offsets": False,
            "payloads": False,
            "positions": True,
            "term_statistics": False,
            "field_statistics": False
        }
    )

    if len(result_tv['term_vectors']) == 0:
        log.info('empty article found for %s', docid)
    else:
        terms_stats = result_tv['term_vectors']['text']['terms']
        tokens_w1 = terms_stats[w1]['tokens']
        tokens_w2 = terms_stats[w2]['tokens']
        pos1 = get_pos_from_tokens(tokens_w1)
        pos2 = get_pos_from_tokens(tokens_w2)
        return shortest_dis(pos1, pos2)


def get_pos_from_tokens(tokens):
    pos = []
    for k in tokens:
        pos.append(k['position'])
    return pos

def shortest_dis(pos1, pos2):
    dis = 1000000000
    for p1 in pos1:
        for p2 in pos2:
            dis = min(dis, abs(p1 - p2))
    return dis

def avg_dis(pos1, pos2):
    dis = 0
    for p1 in pos1:
        for p2 in pos2:
            if p2 > p1:
                dis += 1.0 / abs(p1 - p2)
    return dis



if __name__ == '__main__':
    print (type(bigram_distance('0', '1969', '60')))