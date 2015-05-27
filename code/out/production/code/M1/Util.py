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

