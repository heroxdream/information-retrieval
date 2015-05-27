__author__ = 'Xuan Han'

import logging

from Constants import DATA_SET, LOG_DIR

from elasticsearch import Elasticsearch


def print_hits(results):
    """ Simple utility function to print results of a search query. """
    # print (results)
    print('=' * 80)
    print('Total %d found in %dms' % (results['hits']['total'], results['took']))
    if results['hits']['hits']:
        print('-' * 80)
    for hit in results['hits']['hits']:
        # get created date for a repo and fallback to authored_date for a commit
        print('/%s/%s/%s :  %s  %s \n   %s' % (
            hit['_index'], hit['_type'], hit['_id'],
            hit['_source']['docno'],
            hit['_source']['text'].replace('\n', ' '),
            hit['_explanation']))
    print()


if __name__ == '__main__':
    # get trace logger and set level
    tracer = logging.getLogger('elasticsearch.trace')
    tracer.setLevel(logging.INFO)
    tracer.addHandler(logging.FileHandler(LOG_DIR))
    # instantiate es client, connects to localhost:9200 by default
    es = Elasticsearch()

    print('Empty search:')
    # print_hits(es.search(index=DATA_SET))

    print('Computer scientist:')
    result_cs = es.search(
        index=DATA_SET,
        body={
            'query': {
                'filtered': {
                    'query': {
                        "match_all": {}
                    },
                    'filter': {
                        'bool': {
                            'must': [
                                {
                                    'term': {
                                        'text': 'computer'
                                    }
                                },
                                {
                                    'term': {
                                        'text': 'scientist'
                                    }
                                }
                            ]

                        }
                    }
                }
            },
            'explain': True,
            'size': 10
        }
    )
    print_hits(result_cs)

    print('Search: "Weather"')
    result_w = es.search(
        index=DATA_SET,
        body={
            "query": {
                "filtered": {
                    "query": {
                        "match": {
                            "text": "science"
                        }
                    },
                    "filter": {
                        "term": {
                            "text": "computer"
                        }
                    }
                }
            },
            "explain": True,
            "size": 10
        }
    )
    print_hits(result_w)
