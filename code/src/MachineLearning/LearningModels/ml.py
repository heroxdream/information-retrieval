#!/usr/bin/env python

from liblinearutil import *
from collections import defaultdict

y, x = svm_read_problem('../ap89_training.txt')
y2, x2 = svm_read_problem('../ap89_testing.txt')
m = train(y, x, '-s 4')
p_label, p_acc, p_val = predict(y, x, m)
p_label2, p_acc2, p_val2 = predict(y2, x2, m)

training_list = []
testing_list = []
for v in p_val: training_list.append(v[0])
for v in p_val2: testing_list.append(v[0])

print len(training_list)
print len(testing_list)

training_head = open('../training_head', 'r')
testing_head = open('../testing_head', 'r')

training_map = defaultdict(dict)
testing_map = defaultdict(dict)

counter = 0
while True:
	line = training_head.readline().strip()
	if line == '': break
	line = line.split()[0]
	qid, id1, id2 = line.split('-')
	docid = id1 + '-' + id2
	print docid
	training_map[qid][docid] = training_list[counter]
	counter += 1


counter = 0
while True:
	line = testing_head.readline().strip()
	if line == '': break
	line = line.split()[0]
	qid, id1, id2 = line.split('-')
	docid = id1 + '-' + id2
	print docid
	testing_map[qid][docid] = testing_list[counter]
	counter += 1


print len(testing_map)
print len(training_map)

output_training = open('output_training.txt', 'w')
for qid in training_map:
	for docid in sorted(training_map[qid], key=training_map[qid].get):
		line = '{} {} {} {} {} {}\n'.format(qid, 'Q0', docid, '0', training_map[qid][docid], 'exp')
		output_training.write(line)
output_training.close()

output_testing = open('output_testing.txt', 'w')
for qid in testing_map:
	for docid in sorted(testing_map[qid], key=testing_map[qid].get):
		line = '{} {} {} {} {} {}\n'.format(qid, 'Q0', docid, '0', testing_map[qid][docid], 'exp')
		output_testing.write(line)
output_testing.close()



