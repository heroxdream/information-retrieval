__author__ = 'Xuan Han'

from M1.DataLoader import doc_length, term_freq

from M1.Constants import V

from M1.Models.IRModel import IRModel

from M1.LOG import log

import scipy as sp


class LMLaplace(IRModel):
    def __init__(self, query_str):
        IRModel.__init__(self, query_str)
        self.threshold = 10000

    def score(self):
        self.uniq_docids()
        for term in self.query_terms:
            if not term_freq.has_key(term):
                log.info('term %s is not found in term_freq, skip ...', term)
                continue
            term_docs_freq = term_freq[term]
            ttf = cf(term_docs_freq)
            for docid in self.rank_list:
                tf = 0
                if term_docs_freq.has_key(docid):
                    tf = term_docs_freq[docid]
                score_this_term = sp.log2(self.score_once(tf, docid) + self.score_twice(ttf))
                self.rank_list[docid] += score_this_term

    def uniq_docids(self):
        for term in self.query_terms:
            if not term_freq.has_key(term):
                log.info('term %s is not found in term_freq, skip ...', term)
                continue
            term_docs_freq = term_freq[term]
            log.info('term %s found in %s articles ...', term, len(term_docs_freq))
            for docid in term_docs_freq:
                docid = str(docid)
                self.rank_list[docid] = 0

    def score_once(self, tf, docid):
        return (tf + 1) * 1.0 / (doc_length[docid] + V)

    def score_twice(self, df):
        return 0


def cf(term_docs_freq):
    counter = 0
    for doc_id in term_docs_freq:
        counter += term_docs_freq[doc_id]
    return counter

