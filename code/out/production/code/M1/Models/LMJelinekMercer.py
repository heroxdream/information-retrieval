__author__ = 'Xuan Han'

from M1.DataLoader import doc_length

from M1.Constants import AVG_D, D

from LMLaplace import LMLaplace


class LMJelinekMercer(LMLaplace):

    def __init__(self, query):
        LMLaplace.__init__(self, query)
        self.lam = 0.5
        self.CD = AVG_D * D

    def score_once(self, tf, docid):
        return self.lam * tf / doc_length[docid]

    def score_twice(self, ttf):
        return (1 - self.lam) * ttf / self.CD
