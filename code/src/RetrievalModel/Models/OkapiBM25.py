__author__ = 'Xuan Han'

from RetrievalModel.DataLoader import doc_length

from RetrievalModel.Constants import AVG_D, D

from RetrievalModel.Models.IRModel import IRModel

import scipy as sp


class OkapiBM25(IRModel):
    def __init__(self, query_str):
        IRModel.__init__(self, query_str)
        self.k1 = 2
        self.k2 = 500
        self.b = 0
        self.threshold = 10000

    def score_once(self, tf, docid):
        part1 = (tf + tf * self.k1) * 1.0 / (tf + self.k1 * ((1 - self.b) + self.b * (doc_length[docid] / AVG_D)))
        part2 = (1 + self.k2 * 1) * 1.0 / (1 + self.k2)
        return part1 * part2

    def score_twice(self, df):
        return sp.log2((D * 1.0 + 0.5) / (df + 0.5))
