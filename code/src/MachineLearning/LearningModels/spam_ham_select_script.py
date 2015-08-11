__author__ = 'hanxuan'
from SparseMatrixReader import SparseMatrixReader
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report

training_file_path = '../Data/spam_ham_train_select.txt'
testing_file_path = '../Data/spam_ham_test_select.txt'

smr_train = SparseMatrixReader(training_file_path)
smr_test = SparseMatrixReader(testing_file_path)

logreg = LogisticRegression(max_iter=5000, solver='liblinear', verbose=True)
print 'LogisticRegression config:'
print logreg.get_params()
logreg.fit(smr_train.feature_matrix, smr_train.labels)
logreg_score_train = logreg.score(smr_train.feature_matrix, smr_train.labels)
print 'LogisticRegression precision train: {}'.format(logreg_score_train)
logreg_score_test = logreg.score(smr_test.feature_matrix, smr_test.labels)
print 'LogisticRegression precision test: {}'.format(logreg_score_test)
print 'RAW LogisticRegression performance:'
print classification_report(smr_test.labels, logreg.predict(smr_test.feature_matrix))
logreg_test_results = logreg.predict_proba(smr_test.feature_matrix).tolist()
test_head_file = open('../Data/spam_ham_test_head_select.txt', 'r', 1024 * 1024 * 8)
content = test_head_file.read()
file_names = content.split('\n')
print len(logreg_test_results), len(file_names)
prob_result_map = {}
for i in xrange(len(logreg_test_results)):
    prob_result_map[file_names[i]] = logreg_test_results[i]

counter = 0
for file_name in sorted(prob_result_map, key=prob_result_map.get, reverse=True):
    print file_name, prob_result_map[file_name]
    counter += 1
    if counter == 10: break