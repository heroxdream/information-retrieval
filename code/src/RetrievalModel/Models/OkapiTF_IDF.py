__author__ = 'Xuan Han'

from RetrievalModel.Models.OkapiTF import OkapiTF

import scipy as sp

from RetrievalModel.Constants import D

class OkapiTfIDF(OkapiTF):
    def __init__(self, query_str):
        OkapiTF.__init__(self, query_str)
        self.threshold = 10000

    def score_twice(self, df):
        return sp.log2(D * 1.0 / df)


