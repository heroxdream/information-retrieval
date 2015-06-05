__author__ = 'Xuan Han'

from RetrievalModel.Stemmer import PorterStemmer

from RetrievalModel.Constants import MEAN_LESS, SAFE_WORD, DESC_WORDS, STOP_WORDS, STEM, STRIP_S, DEL_BIG

from RetrievalModel.Util import *

from RetrievalModel.DataLoader import docs_freq, term_freq

import string

p = PorterStemmer()


class IRModel:

    top_count = 1000

    def __init__(self, query_str):

        query_str = string.lower(strip_dot(query_str))

        log.info('query: %s', query_str)

        initial_terms = string.split(query_str, " ")

        self.query_id = string.rstrip(initial_terms[0], '.')
        log.info('query id: %s', self.query_id)

        self.query_terms = initial_terms[1:]

        self.rank_list = dict()
        self.threshold = 0
        self.del_term = []

    def term_regulate(self):
        terms = self.query_terms
        term2 = []
        for term in terms:
            term2 = term2 + string.split(term, "-")

        term3 = []
        for term in term2:
            term = strip_punctuation(term)
            if term in STOP_WORDS or term in DESC_WORDS:
                continue

            if STRIP_S:
                term = string.rstrip(term, 's')

            if term in DESC_WORDS or term in STOP_WORDS:
                continue

            if STEM:
                term = p.stem(term, 0, len(term) - 1)

            term3.append(term)

        self.query_terms = []

        for term in term3:

            if term in SAFE_WORD:
                self.query_terms.append(term)
                continue

            if DEL_BIG and docs_freq.has_key(term) and docs_freq[term] > self.threshold:
                self.del_term.append(term)
                continue

            if term in MEAN_LESS:
                self.del_term.append(term)
                continue

            self.query_terms.append(term)
        log.info('query term: %s', self.query_terms)
        log.info('delet term: %s', self.del_term)

    def score(self):
        for term in self.query_terms:
            if not term_freq.has_key(term):
                log.info('term %s is not found in term_freq, skip ...', term)
                continue
            term_docs_freq = term_freq[term]
            df = len(term_docs_freq)
            log.info('term %s found in %s articles ...', term, df)
            for docid in term_docs_freq:
                docid = str(docid)
                tf = term_docs_freq[docid]

                score_this_term = self.score_once(tf, docid) * self.score_twice(df)

                if docid in self.rank_list:
                    doc_current_score = self.rank_list[docid] + score_this_term
                    self.rank_list[docid] = doc_current_score
                else:
                    self.rank_list[docid] = score_this_term

    def score_once(self, tf, docid):
        raise Exception('score_once must be implemented ...')

    def score_twice(self, df):
        raise Exception('score_twice must be implemented ...')

    def print_result(self, file_path):
        output = open(file_path, 'a')

        log.info('Totally %s articles ranked, now output top %s', len(self.rank_list), IRModel.top_count)
        counter = 1
        for doc_id in sorted(self.rank_list, key=self.rank_list.get, reverse=True):
            line = self.query_id + ' Q0' + get_docno(doc_id) + str(counter) + ' ' + str(self.rank_list[doc_id]) + ' Exp'
            output.write(line + '\n')

            counter += 1
            if counter > IRModel.top_count:
                break
