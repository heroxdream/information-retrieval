__author__ = 'hanxuan'

from RetrievalModel.DataLoader import doc_length

from RetrievalModel.Constants import AVG_D, D

from LMLaplace import LMLaplace

class LMDirichlet(LMLaplace):
    def __int__(self, query_st):
        LMLaplace.__init__(self, query_st)

    def score_once(self, tf, docid):
        global alpha
        alpha = 2000 * 1.0 / (doc_length[docid] + 2000)
        return (1 - alpha) * tf / doc_length[docid]

    def score_twice(self, ttf):
        return alpha * ttf / (AVG_D * D)
