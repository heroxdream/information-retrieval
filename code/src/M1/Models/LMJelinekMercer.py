__author__ = 'Xuan Han'

from M1.DataLoader import doc_length

from M1.Constants import AVG_D, D

from LMLaplace import LMLaplace


class LMJelinekMercer(LMLaplace):

    def __init__(self, query):
        LMLaplace.__init__(self, query)
        self.lam = 0.1
        self.CD = AVG_D * D

    def score_once(self, tf, docid):
        if len(self.query_terms) > 4:
            self.lam = 0.7
        return self.lam * tf / doc_length[docid]

    def score_twice(self, ttf):
        if len(self.query_terms) > 4:
            self.lam = 0.7
        return (1 - self.lam) * ttf / self.CD
