__author__ = 'hanxuan'

import re
import os
import glob
import string
import cPickle as cP
import collections
import time

from Utils.ulog import log
from RetrievalModel.Constants import FILE_DIR
from RetrievalModel.Constants import STOP_WORDS
from CacheReader import CacheReader
from CacheWriter import CacheWriter

# from nltk import LancasterStemmer

from nltk import PorterStemmer

# from nltk import SnowballStemmer

from Index.Constants import *


class IndexBuilder(object):
    global doc_id_counter
    doc_id_counter = 0
    global token_id_counter
    token_id_counter = 0

    TEXT_PTN = r'<TEXT>(.*?)</TEXT>'
    HEAD_PTN = r'<HEAD>(.*?)</HEAD>'

    def __init__(self, output, pattern):
        self.catalog_new = dict()
        self.catalog_old = dict()
        self.index_cache = dict()
        self.doc_id_map = dict()
        self.token_id_map = dict()
        self.doc_len_map = dict()
        # self.stemmer = LancasterStemmer()
        self.stemmer = PorterStemmer()
        # self.stemmer = SnowballStemmer('english')
        self.ptn_field = pattern
        self.output_path = output
        self.gap = 10000
        self.remove_stopwords = True
        self.stem = True
        self.join_cache = 1024 * 1024 * 32

    def pre_precess(self):
        files = os.path.join(self.output_path, '*')
        for f in glob.glob(files):
            os.remove(f)

    def post_process(self):
        self.serialize_catalog()
        self.serialize_doc_map()
        self.serialize_token_map()
        self.serialize_dlen_map()
        return 0

    def get_raw_tokens(self, segment):
        pattern1 = re.compile(r"<DOCNO>(.*?)</DOCNO>")
        doc_id = ''.join(pattern1.findall(segment)).strip()
        pattern2 = re.compile(self.ptn_field, re.M | re.S)
        doc_text = ''.join(pattern2.findall(segment)).strip()
        pattern3 = re.compile(r"(\w+(\.?\w+)*)")
        if doc_id == '' or doc_text == '':
            log.debug('empty id or text found: {}'.format(segment))
        return pattern3.findall(doc_text), doc_id

    def filter_tokens(self, tokens, doc_id):
        tokens_filter = []
        pos_counter = 1
        for token in tokens:
            token = token[0].strip().lower()
            if self.remove_stopwords and token in STOP_WORDS:
                log.debug('stop_word@{}: {}'.format(doc_id, token))
                continue
            if self.stem:
                token = self.stemmer.stem(token)
            log.debug('token: {}@{}'.format(pos_counter, token))
            pos_counter += 1
            tokens_filter.append(token)
        return tokens_filter

    def get_doc_id_int(self, doc_id):
        global doc_id_counter
        if not self.doc_id_map.has_key(doc_id):
            self.doc_id_map[doc_id] = doc_id_counter
            doc_id_counter += 1
        return self.doc_id_map[doc_id]

    def get_token_id_int(self, token):
        global token_id_counter
        if not self.token_id_map.has_key(token):
            self.token_id_map[token] = token_id_counter
            token_id_counter += 1
        return self.token_id_map[token]

    def push_to_cache(self, tokens_filter, doc_id):

        doc_id = self.get_doc_id_int(doc_id)
        self.record_doc_len(doc_id, len(tokens_filter))
        pos_counter = 1
        for token in tokens_filter:
            token = self.get_token_id_int(token)
            if self.index_cache.has_key(token):
                if self.index_cache[token].has_key(doc_id):
                    self.index_cache[token][doc_id].append(pos_counter)
                else:
                    self.index_cache[token][doc_id] = [pos_counter]
            else:
                self.index_cache[token] = {doc_id: [pos_counter]}
            pos_counter += 1
        log.debug(self.index_cache)
        log.debug(self.token_id_map)
        log.debug(self.doc_id_map)
        log.debug(self.doc_len_map)

    def record_doc_len(self, docid_int, increment):
        if not self.doc_len_map.has_key(docid_int):
            self.doc_len_map[docid_int] = 0
        self.doc_len_map[docid_int] += increment

    def process_one_article(self, segment):

        raw = self.get_raw_tokens(segment)

        raw_tokens = raw[0]

        doc_id = raw[1]

        tokens_filter = self.filter_tokens(raw_tokens, doc_id)

        self.push_to_cache(tokens_filter, doc_id)

    def process_one_file(self, str_in):
        segments = string.split(str_in, "</DOC>")
        doc_counter = 0
        for seg in segments:
            if len(seg) < 1 or len(seg.strip()) < 1:
                continue
            self.process_one_article(seg)
            doc_counter += 1
        return doc_counter

    def process(self):
        files = os.path.join(FILE_DIR, 'ap*')
        counter = 0
        file_counter = 0
        total_doc_counter = 0
        for txt_file in glob.glob(files):
            file_current = open(txt_file, "r", 1024 * 1024 * 8)
            doc_count = self.process_one_file(file_current.read())
            file_counter += 1
            total_doc_counter += doc_count
            counter += doc_count
            log.info('{}/({}) files processed, indexed {} documents...'.format(file_counter, len(glob.glob(files)), total_doc_counter))

            if counter >= self.gap or file_counter == len(glob.glob(files)):
                self.combine(total_doc_counter)
                self.index_cache.clear()
                self.catalog_old = self.catalog_new
                self.catalog_new = dict()
                counter = 0

    def combine(self, counter):
        new_file = self.output_path + '/' + str(counter) + '.index'
        if len(glob.glob(os.path.join(self.output_path, '*.index'))) > 0:
            old_file = glob.glob(os.path.join(self.output_path, '*.index'))[0]
            self.join_index(old_file, new_file)
            log.info('join file:\n {} \n and\n {} finished, now remove old file: \n{}'.format(new_file, old_file, old_file))
            os.remove(old_file)
        else:
            self.dump_first_file(new_file)

    def dump_first_file(self, file_path):
        log.info('dumping: {}'.format(file_path))
        output = open(file_path, mode='wb', buffering=IO_CACHE)
        self.catalog_new,catalog_offset = CacheWriter(self.index_cache).write_vb(output)
        output.close()

    def join_index(self, oldfile, newfile):
        input_file = open(oldfile, 'rb', IO_CACHE)
        output_file = open(newfile, 'wb', IO_CACHE)
        cache_groups = self.cache_group()
        log.info('cache_groups: {}'.format(cache_groups))
        for cache in cache_groups:
            bs = input_file.read(cache)
            data_map = CacheReader(bs).bs2data_vb().read_all()
            log.debug('cache group: {}, data_map: {}'.format(cache, data_map))
            self.join_by_maps(data_map, output_file)
        self.append_remain_tokens(output_file)
        log.info('output_file position: {} Mbytes'.format(output_file.tell() * 1.0 / 1024 / 1024))
        output_file.close()
        return 0

    def append_remain_tokens(self, output_file):
        if len(self.index_cache) > 0:
            self.catalog_new, catalog_offset = CacheWriter(self.index_cache).write_vb(output_file, self.catalog_new, output_file.tell())

    def join_by_maps(self, data_map, output_file):
        index_cache_new = dict()
        for token in data_map:
            if self.index_cache.has_key(token):
                index_cache_new[token] = self.combine_pos(token, data_map[token].get_pos_map())
                self.index_cache.pop(token)
            else:
                index_cache_new[token] = data_map[token].get_pos_map()
        log.debug('index_cache_new: {}'.format(index_cache_new))
        self.catalog_new, catalog_offset = CacheWriter(index_cache_new).write_vb(output_file, self.catalog_new, output_file.tell())
        log.info('output_file position: {} Mbytes'.format(output_file.tell() * 1.0 / 1024 / 1024))
        return output_file.tell()

    def combine_pos(self, token, pos_in_data_map):
        log.debug('pos_in_data_map: {}'.format(pos_in_data_map))
        pos_in_cache = self.index_cache[token]
        log.debug('pos_in_cache: {}'.format(pos_in_cache))
        for doc_id_int in pos_in_cache:
            if pos_in_data_map.has_key(doc_id_int):
                exit('error! key:{} exists in data_map!'.format(doc_id_int))
            pos_in_data_map[doc_id_int] = pos_in_cache[doc_id_int]
        log.debug('pos_in_new_data_map: {}'.format(pos_in_data_map))
        return pos_in_data_map

    def cache_group(self):
        sorted_catalog = collections.Counter(self.catalog_old)
        size = []
        for k, v in sorted_catalog.most_common(len(sorted_catalog)):
            size.append(v[1])
        size.reverse()
        groups = []
        accumulate = 0
        for i in range(0, len(size)):
            accumulate += size[i]
            if accumulate > self.join_cache or i == len(size) - 1:
                groups.append(accumulate)
                accumulate = 0
        return groups

    def serialize_catalog(self):
        output_file = open(self.output_path + '/' + CATALOG_FILE, 'wb', IO_CACHE)
        cP.dump(self.catalog_old, output_file, protocol=cP.HIGHEST_PROTOCOL)
        output_file.close()

    def serialize_token_map(self):
        output_file = open(self.output_path + '/' + TOKEN_MAP_FILE, 'wb', IO_CACHE)
        cP.dump(self.token_id_map, output_file, protocol=cP.HIGHEST_PROTOCOL)
        output_file.close()

    def serialize_doc_map(self):
        output_file = open(self.output_path + '/' + DOC_MAP_FILE, 'wb', IO_CACHE)
        cP.dump(self.doc_id_map, output_file, protocol=cP.HIGHEST_PROTOCOL)
        output_file.close()

    def serialize_dlen_map(self):
        output_file = open(self.output_path + '/' + DLEN_MAP_FILE, 'wb', IO_CACHE)
        cP.dump(self.doc_len_map, output_file, protocol=cP.HIGHEST_PROTOCOL)
        output_file.close()


if __name__ == '__main__':

    t1 = time.time()

    builder = IndexBuilder(INDEX_DIR_PORTER, IndexBuilder.TEXT_PTN)
    builder.pre_precess()
    builder.process()
    builder.post_process()

    builder = IndexBuilder(INDEX_DIR_1, IndexBuilder.TEXT_PTN)
    builder.stem = False
    builder.pre_precess()
    builder.process()
    builder.post_process()

    builder = IndexBuilder(INDEX_DIR_2, IndexBuilder.TEXT_PTN)
    builder.remove_stopwords = False
    builder.pre_precess()
    builder.process()
    builder.post_process()

    builder = IndexBuilder(INDEX_DIR_3, IndexBuilder.TEXT_PTN)
    builder.stem = False
    builder.remove_stopwords = False
    builder.pre_precess()
    builder.process()
    builder.post_process()

    t2 = time.time()

    log.info('Total time took: {} min'.format((t2 - t1) * 1.0 / 60))
