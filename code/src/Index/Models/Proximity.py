__author__ = 'hanxuan'

from Model import Model

from RetrievalModel.LOG import log

from MinSpanQueue import MinSpanQueue

from collections import defaultdict

import scipy as sp


class Proximity(Model):
    def __init__(self, query, im):
        Model.__init__(self, query, im)
        self.threshold = 10000
        self.uniq_doc_tokens = defaultdict(set)

    def doc_token_mapping(self):
        for token in self.query_terms:
            if not self.im.token_id_map.has_key(token):
                log.info('term %s is not found in term_freq, skip ...', token)
                continue
            pos_map = self.im.get_term_info(token).get_pos_map()
            for doc_id in pos_map:
                self.uniq_doc_tokens[doc_id].add(token)

    def score(self):
        self.doc_token_mapping()
        for doc_id in self.uniq_doc_tokens:
            tokens = self.uniq_doc_tokens[doc_id]
            pos_list = self.tokens_pos_mapping(tokens, doc_id)
            min_span = MinSpanQueue(pos_list).min_span() + 1
            self.rank_list[doc_id] = 50 * sp.log(len(pos_list)) - sp.log(min_span * 1.0 / self.im.get_doc_len_by_id(doc_id))

    def tokens_pos_mapping(self, tokens, doc_id):
        pos_list = []
        for token in tokens:
            pos = self.im.get_term_info(token).get_pos_map()[doc_id]
            pos_list.append(pos[:])
        return pos_list

if __name__ == '__main__':
    print 1