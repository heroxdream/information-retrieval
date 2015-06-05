__author__ = 'hanxuan'

from Constants import I

from RetrievalModel.LOG import log

import struct

class CacheWriter(object):
    def __init__(self, index_cache):
        self.index_cache = index_cache

    def write(self, output_file, catalog=dict(), catalog_offset=0):
        sequence = []
        counter = 0
        for token in self.index_cache:
            offset_start = counter * I
            term_doc_pos = self.index_cache[token]
            df = len(term_doc_pos)
            cf = 0
            sequence.append(token)
            counter += 1
            sequence.append(cf)
            cf_pos = counter
            counter += 1
            sequence.append(df)
            counter += 1
            for doc in term_doc_pos:
                poss = term_doc_pos[doc]
                cf += len(poss)
                sequence.append(doc)
                sequence.append(len(poss))
                counter += 2
                for pos in poss:
                    sequence.append(pos)
                    counter += 1
            sequence[cf_pos] = cf
            offset_end = counter * I
            catalog[token] = (offset_start + catalog_offset, offset_end - offset_start)
            log.debug('token: {}, cf({}), df({}), offset&size({})'.format(token, cf, df, catalog[token]))
        bs = struct.pack('{}I'.format(counter), *sequence)
        output_file.write(bs)

        log.info('fmt: {}I, write size: {} Mbytes'.format(counter, counter * I * 1.0 / 1024 / 1024))
        log.debug('seq: {}'.format(sequence))

        return catalog, counter * I
