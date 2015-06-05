__author__ = 'hanxuan'

from Model import Model
from Index.Constants import AVG_D

class OkapiTF(Model):
    def __init__(self, query_str, im):
        Model.__init__(self, query_str, im)
        self.alpha = 0.5
        self.beta = 1.5
        self.threshold = 6000

    def score_once(self, tf, docid_int):
        return tf * 1.0 / (tf + self.alpha + self.beta * (self.im.get_doc_len_by_id(docid_int) / AVG_D))

    def score_twice(self, df):
     return 1
