__author__ = 'hanxuan'

from Utils.ulog import log

def uniq_url(data_set, es):

    uniq_url_set = set()

    body={
        "fields": ['url'],
        "query": {
            "match_all": {}
        }
    }

    resp = es.search(index=data_set, doc_type='document',body=body, explain=False, scroll="100m",size=2000)
    scroll_id = resp['_scroll_id']
    while True:
        for i in resp['hits']['hits']:
            url = i['fields']['url'][0]
            uniq_url_set.add(url)
        resp = es.scroll(scroll_id=scroll_id, scroll='100m')
        if len(resp['hits']['hits']) > 0:
            log.info('finish scroll once')
            scroll_id = resp['_scroll_id']
        else:
            log.info('scrollId2: {}'.format(scroll_id))
            break

    return uniq_url_set


def write_to_file(id_docno_map, data_map, file_path):
    out_file = open(file_path, 'w')
    sorted_tuple = sorted(data_map.items(), key=lambda x:x[1], reverse=True)
    counter = 0
    for tpl in sorted_tuple:
        out_file.write('{}\t{}\n'.format(id_docno_map[tpl[0]],tpl[1]))
        counter += 1
        if counter > 500: break
    out_file.close()
