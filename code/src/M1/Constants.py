__author__ = 'Xuan Han'

FILE_DIR = "/Users/hanxuan/Dropbox/neu/summer15/information retrieval/data/AP_DATA/ap89_collection/"

LOG_DIR = '/Users/hanxuan/Dropbox/neu/summer15/information retrieval/log/es.log'

DATA_SET = 'ap_dataset'

STEM = True

STRIP_S = True

DEL_BIG = True

D = 84678

AVG_D = 247.811

V = 176982

DESC_WORDS = ['document', 'must', 'will', 'identify', 'describe', 'discuss', 'report', 'predict', 'include',
              'cite', '', '\n']

MEAN_LESS = ['type', 'move', 'event', 'ongo', 'method', 'actual']

# SAFE_WORD = ['prime', 'militari', 'polit', 'countri', 'financi', 'institut', 'communist', 'industri', 'system', 'armi']

SAFE_WORD = ['financi', '1988', 'communist', 'prime', 'institut', 'armi']

STOP_WORDS_FILE = open('/Users/hanxuan/Dropbox/neu/summer15/information retrieval/data/AP_DATA/stoplist.txt', 'rb')
STOP_WORDS = set()
line = ''
while True:
    line = STOP_WORDS_FILE.readline().strip()
    if line == '':
        break
    STOP_WORDS.add(line)
STOP_WORDS_FILE.close()
print 'stop_words count: ', len(STOP_WORDS)


# this is for a git test
print('this is for a git test')
