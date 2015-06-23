__author__ = 'hanxuan'

import string

from nltk import LancasterStemmer
from nltk import PorterStemmer
from nltk import SnowballStemmer

from RetrievalModel.Models.IRModel import IRModel
from RetrievalModel.Constants import MEAN_LESS, SAFE_WORD, DESC_WORDS, STOP_WORDS, STEM, STRIP_S, DEL_BIG
from RetrievalModel.Util import *
from Utils.log import log


class Model(IRModel):
    def __init__(self, query_str, im):
        IRModel.__init__(self, query_str)
        self.im = im
        self.ls = LancasterStemmer()
        self.p = PorterStemmer()
        self.sb = SnowballStemmer('english')

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
                # term = self.ls.stem(term)
                term = self.p.stem(term)
                # term = self.sb.stem(term)

            term3.append(term)

        self.query_terms = []

        for term in term3:

            if term in SAFE_WORD:
                self.query_terms.append(term)
                continue

            if DEL_BIG and self.im.token_id_map.has_key(term) \
                    and self.im.get_term_info(term).get_df() > self.threshold:
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
            if not self.im.token_id_map.has_key(term):
                log.info('term %s is not found in term_freq, skip ...', term)
                continue
            term_docs_freq = self.im.get_term_info(term).get_pos_map()
            df = len(term_docs_freq)
            log.info('term %s found in %s articles ...', term, df)
            for docid_int in term_docs_freq:
                tf = len(term_docs_freq[docid_int])
                score_this_term = self.score_once(tf, docid_int) * self.score_twice(df)

                if docid_int in self.rank_list:
                    doc_current_score = self.rank_list[docid_int] + score_this_term
                    self.rank_list[docid_int] = doc_current_score
                else:
                    self.rank_list[docid_int] = score_this_term

    def print_result(self, file_path):
        output = open(file_path, 'a')

        log.info('Totally %s articles ranked, now output top %s', len(self.rank_list), IRModel.top_count)
        counter = 1
        for doc_id_int in sorted(self.rank_list, key=self.rank_list.get, reverse=True):
            line = '{} Q0 {} {} {} EXP'.format(self.query_id, self.im.get_docno_by_int_id(doc_id_int), str(counter), str(self.rank_list[doc_id_int]))
            output.write(line + '\n')

            counter += 1
            if counter > IRModel.top_count:
                break
