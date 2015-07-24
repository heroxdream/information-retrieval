__author__ = 'hanxuan'

import os
import glob
from collections import defaultdict

data_dir = '/Users/hanxuan/Dropbox/neu/tools/github/ir/code/src/RetrievalModel/Models/Results'

qrels_file = 'qrels.adhoc.51-100.AP89.txt'

test_set = ['58', '68', '91', '94', '71']

files = os.path.join(data_dir, 'output.*')

feature_map = defaultdict(dict)
feature_count = 0
for one_file in glob.glob(files):
    in_file = open(one_file, 'r')
    while True:
        line = in_file.readline()
        if line == '': break
        qid, dummy, docid, rank, score, exp = line.strip().split()
        score = float(score)
        key = qid + '-' + docid
        feature_map[key][feature_count] = score
    feature_count += 1
    print '{} loaded...'.format(one_file)

print 'feature_map size {}'.format(len(feature_map))

label_map = dict()
in_file = open(data_dir + '/' + qrels_file, 'r')
while True:
    line = in_file.readline()
    if line == '': break
    qid, dummy, docid, label = line.strip().split()
    label = float(label)
    key = qid + '-' + docid
    if key in feature_map: label_map[key] = label

print 'label_map size {}'.format(len(label_map))


mean_map = defaultdict(float)
std_map = defaultdict(float)
span_map = defaultdict(float)
feature_max = defaultdict(float)
feature_min = defaultdict(float)
for key in label_map:
    features = feature_map[key]
    for feature_id in features:
        mean_map[feature_id] += features[feature_id]
        feature_max[feature_id] = max(features[feature_id], feature_max[feature_id])
        feature_min[feature_id] = min(features[feature_id], feature_min[feature_id])

for key in feature_max:
    span_map[key] = feature_max[key] - feature_min[key]

for key in mean_map:
    mean_map[key] /= len(label_map)

for key in label_map:
    features = feature_map[key]
    for feature_id in features:
        std_map[feature_id] += pow(features[feature_id] - mean_map[feature_id], 2)

for key in std_map:
    std_map[key] = pow(std_map[key], 0.5)

training_file = open('ap89_training.txt', 'w')
test_file = open('ap89_testing.txt', 'w')
training_head = open('training_head', 'w')
testing_head = open('testing_head', 'w')
training_file_line_num = 0
testing_file_line_num = 0
for key in label_map:
    qid = key.split('-')[0]
    features = feature_map[key]
    line = str(label_map[key]) + ' '
    features_str = []
    for feature_id in features:
        features_str.append(str(feature_id) + ':' + str((features[feature_id] - feature_min[feature_id]) / span_map[feature_id]))
    line += ' '.join(features_str) + '\n'
    if qid in test_set:
        test_file.write(line)
        testing_file_line_num += 1
        testing_head.write('{} {}\n'.format(key, testing_file_line_num))
    else:
        training_file.write(line)
        training_file_line_num += 1
        training_head.write('{} {}\n'.format(key, training_file_line_num))

training_file.close()
test_file.close()
