__author__ = 'hanxuan'

from TokenInfo import TokenInfo

from Index.Constants import I, B

from VB import vb_decode

import struct

class CacheReader(object):
    def __init__(self, byte_array):
        self.bs = byte_array
        self.data = None
        self.pointer = 0

    def bs2data(self):
        self.data = struct.unpack('{}I'.format(len(self.bs) / I), self.bs)
        return self

    def bs2data_vb(self):
        self.data = vb_decode(self.bs)
        return self

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
