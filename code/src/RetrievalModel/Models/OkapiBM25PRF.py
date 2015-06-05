__author__ = 'Xuan Han'

from RetrievalModel.Models.OkapiBM25 import OkapiBM25

from RetrievalModel.DataLoader import docs_freq

from RetrievalModel.Constants import D

from RetrievalModel.Stemmer import PorterStemmer

from RetrievalModel.Util import *

import scipy as sp


class OkapiBM25PRF(OkapiBM25):
    p = PorterStemmer()

    def __init__(self, query_str):
        OkapiBM25.__init__(self, query_str)
        self.k = 20
        self.topN = 4
        self.alpha = 0.33
        self.loop_round = 3

    def select_term(self, loop_round):
        terms_tf = dict()
        counter = 0
        for docid in sorted(self.rank_list, key=self.rank_list.get, reverse=True):
            doc_terms_tf = get_all_tf_by_docid(docid)
            for term in doc_terms_tf:
                if terms_tf.has_key(term):
                    terms_tf[term] += doc_terms_tf[term]
                else:
                    terms_tf[term] = doc_terms_tf[term]
            counter += 1
            if counter >= self.k * pow(loop_round, 0.5):
                break

        # okapi_tf_idf = OkapiTfIDF('')
        for term in terms_tf:
            terms_tf[term] *= sp.log2(D / docs_freq[term])
            # terms_tf[term] = okapi_tf_idf.score_once(terms_tf[term], docid) * okapi_tf_idf.score_twice(docs_freq[term])

        counter = 0
        tmp_terms = self.query_terms
        self.query_terms = []
        for term in sorted(terms_tf, key=terms_tf.get, reverse=True):
            if term not in self.query_terms:
                self.query_terms.append(term)
            counter += 1
            if counter >= self.topN * pow(loop_round, 0.5):
                break

        self.term_regulate()

        for term in self.query_terms:
            tmp_terms.append(term)
            log.info('query id: %s, new term %s -> query_terms ...', self.query_id, term)

        self.query_terms = tmp_terms
        self.rank_list = dict()

    def score_again(self):
        self.select_term(1)
        self.score()

    def loop(self):

        score_list = dict()
        for i in range(0, D, 1):
            score_list[str(i)] = 0

        for i in range(0, self.loop_round, 1):
            log.info('query for %s: round %s start ...', self.query_id, i)
            self.score()
            for docid in self.rank_list:
                score_list[docid] += self.rank_list[docid] * pow(self.alpha, i)
            self.select_term(i + 1)

        self.rank_list = score_list
