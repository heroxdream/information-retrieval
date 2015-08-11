# -*- coding: utf-8 -*-
__author__ = 'hanxuan'

import os
import glob
from Utils.ues import es
import string
import random
import numpy as np
import cPickle
import pprint
import matplotlib.pyplot as plt
from collections import defaultdict

DATA_SET = 'spam_ham'
SPAM = 'spam'
HAM = 'ham'


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
                    "text": {
                        "type": "string",
                        "store": True,
                        "index": "analyzed",
                        "term_vector": "with_positions_offsets_payloads",
                        "analyzer": "my_english"
                    },
                    "split": {
                        "type": "string",
                        "store": True,
                        "index": "not_analyzed",
                    },
                    "label": {
                        "type": "string",
                        "store": False,
                        "index": "not_analyzed"
                    }
                }
            }
        }
    )

file_label_map = {}


def read_label():
    label_path = '/Users/hanxuan/Downloads/trec07p/full/index'
    in_file = open(label_path, 'r')
    while True:
        line = string.strip(in_file.readline())
        if line == '': break
        elements = string.split(line)
        label = elements[0]
        file_name = string.split(elements[1], '/')[2]
        file_label_map[file_name] = label


def index():
    folder_path = '/Users/hanxuan/Downloads/trec07p/data'
    files = os.path.join(folder_path, 'inmail.*')
    counter = 0
    for txt_file in glob.glob(files):
        in_file = open(txt_file, 'r')
        content = string.strip(string.lower(in_file.read()))
        content = content.decode('utf-8', 'ignore')
        # text = ''.join(string.split(content, 'lines:')[1:])
        text = content
        file_name = txt_file.split('/')[6]
        label = file_label_map[file_name]
        split = 'train'
        if random.random() > 0.8: split = 'test'
        doc = dict(text=text, label=label, split=split)
        res = es.index(index=DATA_SET, doc_type='document', id=file_name, body=doc, timeout=60)
        if not res['created']: print 'insert error'

        counter += 1
        if counter % 2000 == 0: print '{} / {} files processed'.format(counter, len(glob.glob(files)))

word_freq = {}
def words():
    for i in xrange(1, 75420):
        if i % 2000 == 0: print '{} / {} files processed...'.format(i, 75419)
        result_tv = es.termvector(
            index=DATA_SET,
            doc_type='document',
            id='inmail.' + str(i),
            fields=['text'],
            body={
                "offsets": False,
                "payloads": False,
                "positions": False,
                "term_statistics": False,
                "field_statistics": False
            }
        )
        try:
            terms_stats = result_tv['term_vectors']['text']['terms']
            for term in terms_stats:
                if term not in word_freq: word_freq[term] = 0
                word_freq[term] += terms_stats[term]['term_freq']
        except Exception, e:
            print e

def matrix():
    in_put = open('word_index.cpkl', 'rb', 1024 * 1024 * 8)
    word_index = cPickle.load(in_put)

    train_file = open('spam_ham_train.txt', 'w', 1024 * 1024 * 32)
    test_file = open('spam_ham_test.txt', 'w', 1024 * 1024 * 32)

    train_head = open('spam_ham_train_head.txt', 'w', 1024 * 1024 * 32)
    test_head = open('spam_ham_test_head.txt', 'w', 1024 * 1024 * 32)

    for i in xrange(1, 75420):

        if i % 2000 == 0: print '{} / {} files processed...'.format(i, 75419)

        docid = 'inmail.' + str(i)

        result_gen = es.search(
            index=DATA_SET,
            doc_type='document',
            fields=["label", "split"],
            body={
                'query': {
                    'match':{
                        '_id':docid
                    }
                }
            }
        )
        label = result_gen['hits']['hits'][0]['fields']['label'][0]
        split = result_gen['hits']['hits'][0]['fields']['split'][0]
        line = []
        if label == 'ham':
            line.append('1')
        else:
            line.append('0')

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
        terms_stats = result_tv['term_vectors']['text']['terms']
        temp_dict = {}
        for term in terms_stats:
            if term in word_index:
                temp_dict[word_index[term]] = terms_stats[term]['term_freq']
        for k in sorted(temp_dict):
            line.append(str(k) + ':' + str(temp_dict[k]))
        line_str = ' '.join(line)

        if split == 'train':
            train_file.write(line_str + '\n')
            train_head.write(docid + '\n')
        else:
            test_file.write(line_str + '\n')
            test_head.write(docid + '\n')

    train_file.close()
    test_file.close()
    train_head.close()
    test_head.close()


# es.indices.delete(index=DATA_SET, ignore=[400, 404])
# create_index(es)
# read_label()
# index()
# words()
# matrix()

# in_put = open('word_freq.cpkl', 'rb', 1024 * 1024 * 8)
# word_freq = cPickle.load(in_put)
#
# bins = [1, 2, 5, 10, 20, 50, 100, 200, 500, 1000, 2000, 5000, 10000, 20000, 50000]
# freq = word_freq.values()
# hist = np.histogram(freq, bins, density=False)
# print hist
#
# x = hist[1]
# y = hist[0]
# print x
# print y
# print 'len x: ', len(x)
# print 'len y: ', len(y)
#
# plt.plot(x[0:len(x) - 1], y)
# # plt.show()
#
# word_index = {}
# index_counter = 1
# for k, v in word_freq.iteritems():
#     if v > 1:
#         word_index[k] = index_counter
#         index_counter += 1
#
# output = open('word_index.cpkl', 'wb', 1024 * 1024 * 8)
# cPickle.dump(word_index, output, protocol=cPickle.HIGHEST_PROTOCOL)
# output.close()


# in_put = open('word_index.cpkl', 'rb', 1024 * 1024 * 8)
# word_index = cPickle.load(in_put)
# index_word = {}
# for word in word_index:
#     index_word[word_index[word]] = word
#
# out_put = open('index_word.cpkl', 'wb', 1024 * 1024 * 8)
# cPickle.dump(index_word, out_put, protocol=cPickle.HIGHEST_PROTOCOL)
# out_put.close()


def matrix_selected():
    in_file = open('spam_words.txt', 'r')
    content = in_file.read()
    spam_keywords = content.split('\n')
    phrase_index_map = {}
    index_phrase_map = {}
    counter = 0
    for word in spam_keywords:
        phrase_index_map[word] = counter
        index_phrase_map[counter] = word
        counter += 1

    doc_feature_map = defaultdict(dict)
    spam_set = set()
    ham_set = set()
    split_map = {}
    train_set = set()
    test_set = set()

    for phrase in phrase_index_map:

        print 'process {}'.format(phrase)

        re = es.search(
            index=DATA_SET,
            doc_type='document',
            fields=["label", "split"],
            size=80000,
            body={
                'query': {
                    'match':{
                        'text':phrase
                    }
                }
            }
        )
        if int(re['hits']['total']) == 0: continue
        # pprint.pprint(re)
        for element in re['hits']['hits']:
            docid = element['_id']
            score = element['_score']
            label = element['fields']['label'][0]
            split = element['fields']['split'][0]
            doc_feature_map[docid][phrase_index_map[phrase]] = score

            if label == 'spam':
                split_map[docid] = '0'
                spam_set.add(docid)
            else:
                ham_set.add(docid)
                split_map[docid] = '1'

            if split == 'train': train_set.add(docid)
            else: test_set.add(docid)

    train_file = open('spam_ham_train_select.txt', 'w', 1024 * 1024 * 32)
    test_file = open('spam_ham_test_select.txt', 'w', 1024 * 1024 * 32)
    train_head = open('spam_ham_train_head_select.txt', 'w', 1024 * 1024 * 32)
    test_head = open('spam_ham_test_head_select.txt', 'w', 1024 * 1024 * 32)

    for docid in train_set:
        line = [split_map[docid]]
        for feature in sorted(doc_feature_map[docid]):
            line.append(str(feature) + ':' + str(doc_feature_map[docid][feature]))
        line_str = ' '.join(line) + '\n'
        train_file.write(line_str)
        train_head.write(docid + '\n')

    for docid in test_set:
        line = [split_map[docid]]
        for feature in sorted(doc_feature_map[docid]):
            line.append(str(feature) + ':' + str(doc_feature_map[docid][feature]))
        line_str = ' '.join(line) + '\n'
        test_file.write(line_str)
        test_head.write(docid + '\n')

    train_file.close()
    test_file.close()
    train_head.close()
    test_head.close()


matrix_selected()
