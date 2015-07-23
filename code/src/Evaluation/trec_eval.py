__author__ = 'hanxuan'


import sys
from collections import defaultdict
from collections import OrderedDict
import math

K = [5,10, 20, 50, 100]

sep = '\t'

qrel = sys.argv[1]
trec = sys.argv[2]

print 'Evaluation: qrel {}, trec: {}'.format(qrel, trec)

qrel_file = open(qrel, 'r')

qrel_map = defaultdict(dict)
rel_counter = {}
while True:
    line = qrel_file.readline()
    if line == '': break
    qid, dummy, docid, score = line.split(sep)
    score = int(score)
    qrel_map[qid][docid] = score

    if score > 0:
        if qid not in rel_counter: rel_counter[qid] = 0
        rel_counter[qid] += 1

trec_file = open(trec, 'r')

ret_counter = 0
trec_map = defaultdict(list)
qids = set()
while True:
    try:
        line = trec_file.readline()
        if line == '': break
        qid, dummy, docid, rank, score, exp = line.split(sep)
        qids.add(qid)
        # print qid, docid, rank, score
        trec_map[qid].append(docid)
    except Exception, e:
        print 'Exception', e

precision_k = defaultdict(OrderedDict)
recall_k = defaultdict(OrderedDict)
F1_k = defaultdict(OrderedDict)
R_precision = {}
AVG_precision = {}
nDCG = {}
pre_rec_map = defaultdict(OrderedDict)

rel_map = {}

for qid in trec_map:
    num_relevant = 0
    k = 0
    AVG_precision[qid] = 0
    nDCG[qid] = 0
    R_precision[qid] = 0
    pre_rec_map[qid][0] = 1
    for docid in trec_map[qid]:
        k += 1
        score = 0
        if qid in qrel_map and docid in qrel_map[qid]:
            score = qrel_map[qid][docid]
            if score > 0: num_relevant += 1

        p = float(num_relevant) / k
        r = float(num_relevant) / rel_counter[qid]

        if p != 0: pre_rec_map[qid][r] = p

        if score > 0: AVG_precision[qid] += num_relevant * 1.0 / k

        nDCG[qid] += float((pow(2, int(score)) - 1)) / math.log(1 + k, 2)

        if p == r and p != 0:
            R_precision[qid] = p
            # print 'p = r: {} @ {} for {}'.format(p, k, qid)

        if k in K:
            precision_k[qid][k] = p
            recall_k[qid][k] = r
            f1 = 0
            if num_relevant > 0: f1 = 2.0 * p * r / (p + r)
            F1_k[qid][k] = f1
            # print '{}, {}, {} @ {}'.format(p, r, f1, k)
    rel_map[qid] = num_relevant
    AVG_precision[qid] /= rel_counter[qid]
    # print 'AVG: {} for {}'.format(AVG_precision[qid], qid)

total_ret = 0
for qid in trec_map: total_ret += len(trec_map[qid])


if len(sys.argv) == 4 and sys.argv[3] == '-q':
    for qid in qids:
        print 'Query id: {}'.format(qid)
        print 'retrieved: {}'.format(len(trec_map[qid]))
        print 'relevant: {}'.format(len(qrel_map[qid]))
        print 'ret_relevant: {}'.format(rel_map[qid])
        print 'AVG precision: {}'.format(AVG_precision[qid])
        print 'R-precision: {}'.format(R_precision[qid])
        print 'nDCG: {}'.format(nDCG[qid])
        for k, v in precision_k[qid].items(): print 'precision @ {}: {}'.format(k, v)
        for k, v in recall_k[qid].items(): print 'recall @ {}: {}'.format(k, v)
        for k, v in F1_k[qid].items(): print 'f1 @ {}: {}'.format(k, v)
        print ''

print 'Total retrieved: {}'.format(total_ret)
print 'Total relevant: {}'.format(sum(map(lambda x:len(x), qrel_map.values())))
print 'Total ret_relevant: {}\n'.format(sum(rel_map.values()))

AVG_TOTAL = float(sum(AVG_precision.values())) / len(AVG_precision)
print 'AVG TOTAL: {}\n'.format(AVG_TOTAL)

AVG_nDCG = float(sum(nDCG.values())) / len(nDCG)
print 'AVG nDCG: {}\n'.format(AVG_nDCG)

AVG_precision_at_k = {}
AVG_recall_at_k = {}
AVG_F1_at_k = {}
for k in K:
    p = 0
    r = 0
    f1 = 0
    for qid in precision_k: p += precision_k[qid][k]
    for qid in recall_k: r += recall_k[qid][k]
    for qid in F1_k: f1 += F1_k[qid][k]
    AVG_precision_at_k[k] = float(p) / len(precision_k)
    AVG_recall_at_k[k] = float(r) / len(recall_k)
    AVG_F1_at_k[k] = float(f1) / len(F1_k)

AVG_R = sum(R_precision.values()) * 1.0 / len(R_precision)

for k in K: print 'AVG precision @ {}: {}'.format(k, AVG_precision_at_k[k])
print ''
for k in K: print 'AVG recall @ {}: {}'.format(k, AVG_recall_at_k[k])
print ''
for k in K: print 'AVG F1 @ {}: {}'.format(k, AVG_F1_at_k[k])
print ''
print 'AVG R-precision: {}'.format(AVG_R)

for qid in pre_rec_map:
    # print qid
    level = 0
    inter_map = OrderedDict()
    out_file = open(qid, 'w')
    for k, v in reversed(pre_rec_map[qid].items()):
        level = max(level, v)
        inter_map[k] = level
    for k, v in reversed(inter_map.items()):
        out_file.write('{} {}\n'.format(k, v))
    out_file.close()
