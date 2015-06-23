__author__ = 'hanxuan'

import scipy as sp

from Index.Constants import V
from Index.Models.Model import Model
from Utils.log import log


class LMLaplace(Model):
    def __init__(self, query_str, im):
        Model.__init__(self, query_str, im)
        self.threshold = 10000

    def score(self):
        self.uniq_docids()
        for term in self.query_terms:
            if not self.im.token_id_map.has_key(term):
                log.info('term %s is not found in term_freq, skip ...', term)
                continue
            term_docs_freq = self.im.get_term_info(term).get_pos_map()
            ttf = self.im.get_term_info(term).get_cf()
            for docid in self.rank_list:
                tf = 0
                if term_docs_freq.has_key(docid):
                    tf = len(term_docs_freq[docid])
                score_this_term = sp.log2(self.score_once(tf, docid) + self.score_twice(ttf))
                self.rank_list[docid] += score_this_term

    def uniq_docids(self):
        for term in self.query_terms:
            if not self.im.token_id_map.has_key(term):
                log.info('term %s is not found in term_freq, skip ...', term)
                continue
            term_docs_freq = self.im.get_term_info(term).get_pos_map()
            log.info('term %s found in %s articles ...', term, len(term_docs_freq))
            for docid in term_docs_freq:
                self.rank_list[docid] = 0

    def score_once(self, tf, docid):
        return (tf + 1) * 1.0 / (self.im.get_doc_len_by_id(docid) + V)

    def score_twice(self, df):
        return 0
