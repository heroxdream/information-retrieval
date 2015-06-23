__author__ = 'hanxuan'


from Utils.es import es

DATA_SET = 'aiw'

def create_index(client):
    # create empty index
    client.indices.create(
        index=DATA_SET,
        body={
            'settings': {
                "index": {
                    "store": {
                        "type": "default"
                    },
                    "number_of_shards": 1,
                    "number_of_replicas": 1
                },
                # custom analyzer for analyzing file paths
                'analysis': {
                    "analyzer": {
                        "my_english": {
                            "type": "english",
                            "stopwords_path": "stoplist.txt"
                        }
                    }
                }
            }
        },
        # ignore already existing index
        ignore=400
    )

    client.indices.put_mapping(
        index=DATA_SET,
        doc_type='document',
        body={
            'document': {
                "properties": {
                    "url": {
                        "type": "string",
                        "store": True,
                        "index": "no"
                    },
                    "header": {
                        "type": "string",
                        "store": True,
                        "index": "no"
                    },
                    "html": {
                        "type": "string",
                        "store": True,
                        "index": "no"
                    },
                    "text": {
                        "type": "string",
                        "store": True,
                        "index": "analyzed",
                        "term_vector": "with_positions_offsets_payloads",
                        "analyzer": "my_english"
                    },
                    "title": {
                        "type": "string",
                        "store": True,
                        "index": "analyzed",
                        "term_vector": "with_positions_offsets_payloads",
                        "analyzer": "my_english"
                    },
                    "out_links": {
                        "type": "string",
                        "store": False,
                        "index": "no"
                    },
                    "in_links": {
                        "type": "string",
                        "store": False,
                        "index": "no"
                    }
                }
            }
        }
    )

if __name__ == '__main__':
    es.cluster.health(wait_for_status='yellow', request_timeout=5)
    es.indices.delete(index=DATA_SET, ignore=[400, 404])
    create_index(es)




    # if spider.finished_page.value > config.max_tasks:
    #     log.info("########### Tasks Done, EXIT ###########")
    #     exit(0)