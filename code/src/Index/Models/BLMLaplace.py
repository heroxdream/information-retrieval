__author__ = 'hanxuan'

# from RetrievalModel.DataLoader import doc_length, term_freq

from LMLaplace import LMLaplace, V

from RetrievalModel.Util import shortest_dis

import scipy as sp


class BLMLaplace(LMLaplace):
    def __init__(self, query_str, im):
        LMLaplace.__init__(self, query_str, im)
        self.parent = LMLaplace('', im)

    def score(self):
        self.uniq_docids()

        fst_term = self.query_terms[0]
        term_docs_freq = self.im.get_term_info(fst_term).get_pos_map()
        for docid in self.rank_list:
            tf = 0
            if term_docs_freq.has_key(docid):
                tf = len(term_docs_freq[docid])
            score_this_term = sp.log2(self.parent.score_once(tf, docid))
            self.rank_list[docid] += score_this_term

        previous = 0
        for term_current in self.query_terms[1:]:
            term_previous = self.query_terms[previous]
            previous += 1

            if not (self.im.token_id_map.has_key(term_previous) and self.im.token_id_map.has_key(term_current)):
                continue

            term_previous_docs_freq = self.im.get_term_info(term_previous).get_pos_map()
            term_current_docs_freq = self.im.get_term_info(term_current).get_pos_map()

            for docid in self.rank_list:
                tf_w1 = 0
                distance_score = sp.inf
                if term_previous_docs_freq.has_key(docid):
                    tf_w1 = len(term_previous_docs_freq[docid])
                    distance_score = self.im.get_doc_len_by_id(docid)
                    if term_current_docs_freq.has_key(docid):
                        distance_score = shortest_dis(term_previous_docs_freq[docid], term_current_docs_freq[docid])
                score_this_term = sp.log2(self.score_once(tf_w1, distance_score))
                self.rank_list[docid] += score_this_term

    def score_once(self, tf_w1, dis_w1_w2):
        return (1.0 / dis_w1_w2 + 1) / (tf_w1 + V)
