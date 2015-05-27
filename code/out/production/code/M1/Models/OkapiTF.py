__author__ = 'Xuan Han'

from M1.DataLoader import doc_length

from M1.Constants import AVG_D


from M1.Models.IRModel import IRModel


class OkapiTF(IRModel):
    def __init__(self, query_str):
        IRModel.__init__(self, query_str)
        self.alpha = 0.5
        self.beta = 1.5
        self.threshold = 6000

    def score_once(self, tf, docid):
        return tf * 1.0 / (tf + self.alpha + self.beta * (doc_length[docid] / AVG_D))

    def score_twice(self, df):
        return 1
