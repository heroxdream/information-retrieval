__author__ = 'hanxuan'

from Index.Constants import INDEX_DIR_PORTER as INDEX_DIR

from Index.Constants import I, CATALOG_FILE, IO_CACHE, TOKEN_MAP_FILE, DOC_MAP_FILE, DLEN_MAP_FILE

import cPickle as cP

import pylru

import glob

import os

import struct

from CacheReader import CacheReader

from RetrievalModel.LOG import log


class IndexManager(object):
    def __init__(self):
        self.catalog_map = None
        self.doc_id_map = None
        self.id_doc_map = dict()
        self.dlen_map = None
        self.token_id_map = None
        self.index_file = None
        self.mem_cache = pylru.lrucache(10000)
        self.load_meta()

    def load_meta(self):
        catalog_file = open(INDEX_DIR + '/' + CATALOG_FILE, 'rb', IO_CACHE)
        self.catalog_map = cP.load(catalog_file)
        doc_map_file = open(INDEX_DIR + '/' + DOC_MAP_FILE, 'rb', IO_CACHE)
        self.doc_id_map = cP.load(doc_map_file)
        for doc_no in self.doc_id_map:
            self.id_doc_map[self.doc_id_map[doc_no]] = doc_no
        dlen_map_file = open(INDEX_DIR + '/' + DLEN_MAP_FILE, 'rb', IO_CACHE)
        self.dlen_map = cP.load(dlen_map_file)
        token_map_file = open(INDEX_DIR + '/' + TOKEN_MAP_FILE, 'rb', IO_CACHE)
        self.token_id_map = cP.load(token_map_file)
        index_file_path = glob.glob(os.path.join(INDEX_DIR, '*.index'))[0]
        self.index_file = open(index_file_path, 'rb', IO_CACHE)
        assert isinstance(self.catalog_map, dict)
        assert isinstance(self.doc_id_map, dict)
        assert isinstance(self.token_id_map, dict)
        assert isinstance(self.index_file, file)

    def get_term_info(self, token_str):

        if not self.token_id_map.has_key(token_str):
            log.info('token {} does not exist in index'.format(token_str))
            return None
        if not self.mem_cache.__contains__(token_str):
            log.info('push token: {} into cache'.format(token_str))
            self.pull_term_info_into_cache(token_str)
        return self.mem_cache[token_str]

    def pull_term_info_into_cache(self, token_str):
        token_id = self.token_id_map[token_str]
        offset = self.catalog_map[token_id][0]
        size = self.catalog_map[token_id][1]

        log.info('token_id: {}, offset: {}, size: {}'.format(token_id, offset, size))

        self.index_file.seek(offset)
        ba = self.index_file.read(size)
        log.info('ba.len: {}'.format(len(ba)))
        data = struct.unpack('{}I'.format(size / I), ba)
        self.mem_cache[token_str] = CacheReader(data).read_one()[1]
        return token_id

    def get_doc_len_by_id(self, doc_id_int):
        return self.dlen_map[doc_id_int]

    def get_doc_len_by_str(self, doc_id_str):
        return self.dlen_map[self.doc_id_map[doc_id_str]]

    def get_docno_by_int_id(self, doc_id_int):
        return self.id_doc_map[doc_id_int]


if __name__ == '__main__':

    manager = IndexManager()

    print 'V: {}'.format(len(manager.token_id_map))

    counter = 0
    for doc_id in manager.dlen_map:
        counter += manager.dlen_map[doc_id]
    print 'AVG_D: {}'.format(counter * 1.0 / len(manager.dlen_map))

    # print manager.get_term_info('nam')
    # print manager.get_term_info('u.s')
    # print manager.get_term_info('han')
    # print manager.get_term_info('today')
    # print manager.get_term_info('tuesday')
    # print manager.get_term_info('cloudy')
    # print manager.get_term_info('boy')
    # print manager.get_term_info('wednesday')
    # print manager.get_term_info('good')
    # print manager.get_term_info('pilot')
