__author__ = 'hanxuan'

class TokenInfo(object):
    def __init__(self, cf, df, pos_map):
        self.cf = cf
        self.df = df
        self.token_doc_pos_map = pos_map

    def __str__(self):
        return 'cf: {}, df: {}, map: {}'.format(self.cf, self.df, self.token_doc_pos_map)

    def get_cf(self):
        return self.cf

    def get_df(self):
        return self.df

    def get_pos_map(self):
        return self.token_doc_pos_map

    def get_term_poslist_in_doc(self, doc_id_int):
        return self.get_pos_map[doc_id_int]

    def get_term_freq_in_doc(self, doc_id_int):
        return len(self.get_term_poslist_in_doc(doc_id_int))
