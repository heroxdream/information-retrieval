__author__ = 'Xuan Han'

from IRModel import IRModel

from LMJelinekMercer import LMJelinekMercer

from LMLaplace import LMLaplace

from OkapiBM25 import OkapiBM25

from OkapiBM25PRF import OkapiBM25PRF

from OkapiTF import OkapiTF

from OkapiTF_IDF import OkapiTfIDF

from M1.Constants import D

from M1.LOG import log

import collections


class MetaSearch(IRModel):

    def __init__(self, query_str):
        IRModel.__init__(self, query_str)
        self.lmjm = LMJelinekMercer(query_str)
        self.lml = LMLaplace(query_str)
        self.bm = OkapiBM25(query_str)
        self.prf = OkapiBM25PRF(query_str)
        self.tf = OkapiTF(query_str)
        self.tfidf = OkapiTfIDF(query_str)
        for i in range(0, D, 1):
            self.rank_list[str(i)] = 0
        self.bias = 1000

    def term_regulate(self):
        self.lmjm.term_regulate()
        self.lml.term_regulate()
        self.bm.term_regulate()
        self.prf.term_regulate()
        self.tf.term_regulate()
        self.tfidf.term_regulate()

    def score(self):
        self.lmjm.score()
        self.vote(self.lmjm.rank_list, 0.2198, 'lmjm')

        self.lml.score()
        self.vote(self.lml.rank_list, 0.2100, 'lml')

        self.bm.score()
        self.vote(self.bm.rank_list, 0.2673, 'bm')

        self.prf.loop()
        self.vote(self.prf.rank_list, 0.3040, 'prf')

        self.tf.score()
        self.vote(self.tf.rank_list, 0.2108, 'tf')

        self.tfidf.score()
        self.vote(self.tfidf.rank_list, 0.2563, 'tfidf')

    def vote(self, ranklist, weight, model):

        weight = pow(weight, 3)

        ranklist_bias = []

        ranklist = collections.Counter(ranklist)
        for k, v in ranklist.most_common(self.bias):
            ranklist_bias.append(k)

        log.info('meta search: %s: %s \tlist size (%s)/(%s)', self.query_id, model, len(ranklist_bias), len(ranklist))

        point = D
        for doc_id in ranklist_bias:
            self.rank_list[doc_id] += point * 1.0 * weight
            point -= 1

        if point > 0:
            ranklist_set = set(ranklist_bias)
            bonus = point * 1.0 * weight / (D - len(ranklist_bias))
            for doc_id in self.rank_list:
                if doc_id not in ranklist_set:
                    self.rank_list[doc_id] += bonus
