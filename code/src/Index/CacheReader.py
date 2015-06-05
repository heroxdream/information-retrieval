__author__ = 'hanxuan'

from TokenInfo import TokenInfo

class CacheReader(object):
    def __init__(self, data):
        self.data = data
        self.pointer = 0

    def read_one(self):
        token_id = self.data[self.pointer]
        self.pointer += 1
        cf = self.data[self.pointer]
        self.pointer += 1
        df = self.data[self.pointer]
        self.pointer += 1
        # print 'cf: {}, df: {}'.format(cf, df)
        pos_map = dict()
        for i in range(0, df):
            doc_id_int = self.data[self.pointer]
            self.pointer += 1
            tf = self.data[self.pointer]
            self.pointer += 1
            # print 'doc_id: {}, tf: {}'.format(doc_id_int, tf)
            pos_list = []
            for j in range(0, tf):
                pos_list.append(self.data[self.pointer])
                self.pointer += 1
            pos_map[doc_id_int] = pos_list
        return token_id, TokenInfo(cf, df, pos_map)

    def read_all(self):
        token_info_map = dict()
        while self.pointer < len(self.data):
            t_tuple = self.read_one()
            token_info_map[t_tuple[0]] = t_tuple[1]
        return token_info_map
