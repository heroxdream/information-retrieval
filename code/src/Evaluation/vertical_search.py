__author__ = 'hanxuan'
# from Utils.ues import es
from Utils.ucluster import cluster as es

data_set = 'm_x_h_cluster'

top_n = 1000

queries = {'152101': 'Founding fathers',
           '152102': 'independence war causes',
           '152103': 'declaration of independence'}


out_put_file = 'vertical_search.txt'
out_put_stream = open(out_put_file, 'w')

for query_id in queries:
    re = \
        es.search(
            index=data_set,
            body={
                "query": {
                    "query_string": {
                        "default_field": "text",
                        "query": queries[query_id]
                    }
                },
                "size": top_n,
                "fields": ["docno"]
            }
        )
    rank = 1
    for e in re['hits']['hits']:
        line = '{}\t{}\t{}\t{}\t{}\t{}\n'.format(query_id, 'Q0', e['fields']['docno'][0], rank, 'score', 'Exp')
        out_put_stream.write(line)
        rank += 1
