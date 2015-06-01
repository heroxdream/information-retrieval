__author__ = 'hanxuan'

from M1.DataLoader import doc_length

from M1.Constants import AVG_D, D

from LMLaplace import LMLaplace

class LMDirichlet(LMLaplace):
    def __int__(self, query_st):
        LMLaplace.__init__(self, query_st)
        self.lam = 2000
        self.CD = AVG_D * D

    def score_once(self, tf, docid):
        global alpha
        alpha = self.lam * 1.0 / (doc_length[docid] + self.lam)
        return (1 - alpha) * tf / doc_length[docid]

    def score_twice(self, ttf):
        return alpha * ttf / self.CD
