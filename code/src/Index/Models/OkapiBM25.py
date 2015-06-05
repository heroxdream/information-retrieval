__author__ = 'hanxuan'
from Model import Model

from RetrievalModel.Constants import D

from Index.Constants import AVG_D

import scipy as sp


class OkapiBM25(Model):
    def __init__(self, query_str, im):
        Model.__init__(self, query_str, im)
        self.k1 = 2
        self.k2 = 500
        self.b = 0
        self.threshold = 10000

    def score_once(self, tf, docid_int):
        part1 = (tf + tf * self.k1) * 1.0 / \
                (tf + self.k1 * ((1 - self.b) + self.b * (self.im.get_doc_len_by_id(docid_int) / AVG_D)))
        part2 = (1 + self.k2 * 1) * 1.0 / (1 + self.k2)
        return part1 * part2

    def score_twice(self, df):
        return sp.log2((D * 1.0 + 0.5) / (df + 0.5))
