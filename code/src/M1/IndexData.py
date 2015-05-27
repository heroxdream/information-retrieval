__author__ = 'Xuan Han'

import os
import glob
import string
import re
import time
import Article

from Constants import FILE_DIR, DATA_SET

from elasticsearch import Elasticsearch


def seg_to_article(segment):
    pattern1 = re.compile(r"<DOCNO>(.*?)</DOCNO>")
    doc_id = ''.join(pattern1.findall(segment))
    pattern2 = re.compile(r'<TEXT>(.*?)</TEXT>', re.M | re.S)
    doc_text = ''.join(pattern2.findall(segment))
    art = Article(doc_id, doc_text)

    if doc_id == '' or doc_text == '':
        print art.to_string()
        print segment

    return art


def string_to_articles(str_in):
    segments = string.split(str_in, "</DOC>")
    arts = []
    for seg in segments:
        if len(seg) < 1 or len(seg.strip()) < 1:
            continue
        arts.append(seg_to_article(seg))
    return arts


def process():
    files = os.path.join(FILE_DIR, 'ap*')
    arts = []
    for txt_file in glob.glob(files):
        file_current = open(txt_file, "r", 1024)
        arts += string_to_articles(file_current.read())
        print "Processing File: ", txt_file, ", current articles count: ", len(arts)

    return arts


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
                    "docno": {
                        "type": "string",
                        "store": True,
                        "index": "not_analyzed"
                    },
                    "text": {
                        "type": "string",
                        "store": True,
                        "index": "analyzed",
                        "term_vector": "with_positions_offsets_payloads",
                        "analyzer": "my_english"
                    }
                }
            }
        }
    )


def insert_article2indices(client, atcs):
    count = 0
    for article in atcs:
        doc = dict(docno=article.get_id(), text=article.get_text())
        res = client.index(index=DATA_SET, doc_type='document', id=count, body=doc)

        count += 1
        if count % 1000 == 0:
            print count, "articles processed..."

        if not res['created']:
            print "fatal error! index insertion failed..."
            print article.to_string()


if __name__ == '__main__':
    # tracer = logging.getLogger('elasticsearch.trace')
    # tracer.setLevel(logging.INFO)
    # tracer.addHandler(logging.FileHandler(LOG_DIR))

    t1 = time.time()

    es = Elasticsearch()
    es.cluster.health(wait_for_status='yellow', request_timeout=5)
    es.indices.delete(index=DATA_SET, ignore=[400, 404])
    create_index(es)
    print "Article Indices created, now inserting entries..."
    time.sleep(2)

    articles = process()

    insert_article2indices(es, articles)

    es.indices.refresh(index=DATA_SET)

    t2 = time.time()

    print "articles processed, count: ", len(articles), ", time elapsed: ", (t2 - t1) / 60, 'min'
