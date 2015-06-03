__author__ = 'Xuan Han'

import cPickle

from LOG import log

DATA_DIR = '/Users/hanxuan/Dropbox/neu/summer15/information retrieval/data/'


doc_length_file = open(DATA_DIR + 'doc_length.cpkl', 'rb', 1024 * 1024)
doc_length = cPickle.load(doc_length_file)
doc_length_file.close()
assert isinstance(doc_length, dict)
log.info("doc_length_file loaded ...")

total_length = 0
for doc in doc_length:
    total_length += doc_length[doc]
avg_length = (total_length * 1.0) / (len(doc_length))


term_freq_file = open(DATA_DIR + 'term_freq_short.cpkl', 'rb', 1024 * 1024 * 32)
term_freq = cPickle.load(term_freq_file)
assert isinstance(term_freq, dict)
term_freq_file.close()
log.info("term_freq_file loaded ...")

docs_freq_file = open(DATA_DIR + 'docs_freq.cpkl', 'rb', 1024 * 1024)
docs_freq = cPickle.load(docs_freq_file)
assert isinstance(docs_freq, dict)
docs_freq_file.close()
log.info("docs_freq_file loaded ...")


print('*' * 50)
print('data files loaded...')
print('unique term count: ', len(term_freq))
print('doc count: ', len(doc_length))
print('avg_length(doc): ', avg_length)
print('*' * 50)
