__author__ = 'Xuan Han'

from RetrievalModel.DataLoader import doc_length, term_freq

from LMLaplace import LMLaplace, V

from RetrievalModel.Util import bigram_distance

import scipy as sp

class BLMLaplace(LMLaplace):

    def __init__(self, query_str):
        LMLaplace.__init__(self, query_str)

    def score(self):
        self.uniq_docids()

        fst_term = self.query_terms[0]
        term_docs_freq = term_freq[fst_term]
        parent = LMLaplace('<<empty query>>')
        for docid in self.rank_list:
            tf = 0
            if term_docs_freq.has_key(docid):
                tf = term_docs_freq[docid]
            score_this_term = sp.log2(parent.score_once(tf, docid))
            self.rank_list[docid] += score_this_term

        previous = 0
        for term_current in self.query_terms[1:]:
            term_previous = self.query_terms[previous]
            previous += 1

            if not (term_freq.has_key(term_previous) and term_freq.has_key(term_current)):
                continue

            term_previous_docs_freq = term_freq[term_previous]
            term_current_docs_freq = term_freq[term_current]

            for docid in self.rank_list:
                tf_w1 = 0
                distance_score = sp.inf
                if term_previous_docs_freq.has_key(docid):
                    tf_w1 = term_previous_docs_freq[docid]
                    distance_score = doc_length[docid]
                    if term_current_docs_freq.has_key(docid):
                        distance_score = bigram_distance(docid, term_previous, term_current)
                score_this_term = sp.log2(self.score_once(tf_w1, distance_score))
                self.rank_list[docid] += score_this_term

    def score_once(self, tf_w1, dis_w1_w2):
        return (1.0 / dis_w1_w2 + 1) / (tf_w1 + V)
