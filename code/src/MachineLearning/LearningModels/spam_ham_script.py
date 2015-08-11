__author__ = 'hanxuan'
from SparseMatrixReader import SparseMatrixReader
from sklearn.svm import SVC, LinearSVC
from sklearn.linear_model import LogisticRegression
import cPickle
from sklearn.metrics import classification_report

training_file_path = '../Data/spam_ham_train.txt'
testing_file_path = '../Data/spam_ham_test.txt'

smr_train = SparseMatrixReader(training_file_path)
smr_test = SparseMatrixReader(testing_file_path)

# svc = SVC(gamma=0.001, kernel='linear')
# print 'SVC config:'
# print svc.get_params()
# svc.fit(smr_train.feature_matrix, smr_train.labels)
# svc_score_train = svc.score(smr_train.feature_matrix, smr_train.labels)
# print 'SVC precision train: {}'.format(svc_score_train)
# svc_score_test = svc.score(smr_test.feature_matrix, smr_test.labels)
# print 'SVC precision test: {}'.format(svc_score_test)
# # plot_learning_curve(svc, 'SVC Curve', smr_train.feature_matrix, smr_train.labels, n_jobs=4)
# print ''

# lsvc = LinearSVC()
# print 'LinearSVC config:'
# print lsvc.get_params()
# lsvc.fit(smr_train.feature_matrix, smr_train.labels)
# lsvc_score_train = lsvc.score(smr_train.feature_matrix, smr_train.labels)
# print 'LinearSVC precision train: {}'.format(lsvc_score_train)
# lsvc_score_test = lsvc.score(smr_test.feature_matrix, smr_test.labels)
# print 'LinearSVC precision test: {}'.format(lsvc_score_test)
# print ''
# lsvc_test_results = lsvc.predict(smr_test.feature_matrix)
# for i in xrange(10):
#     print lsvc_test_results[i]

# feature_weights = lsvc.coef_[0].tolist()
# print 'feature len: {}'.format(len(feature_weights))
# idx = 0
# feature_map = {}
# for feature in feature_weights:
#     feature_map[idx] = feature
#     idx += 1
#
# in_put = open('../Data/index_word.cpkl', 'rb', 1024 * 1024 * 8)
# index_word = cPickle.load(in_put)
# print 'index_word len: {}'.format(len(index_word))
#
# counter = 0
# for top_feature in sorted(feature_map, key=feature_map.get, reverse=True):
#     try:
#         print top_feature, index_word[top_feature].decode('utf-8'), feature_map[top_feature]
#         counter += 1
#         if counter == 50: break
#     except Exception, e:
#         print e

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
test_head_file = open('../Data/spam_ham_test_head.txt', 'r', 1024 * 1024 * 8)
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


feature_weights = logreg.coef_[0].tolist()
print 'feature len: {}'.format(len(feature_weights))
idx = 0
feature_map = {}
for feature in feature_weights:
    feature_map[idx] = feature
    idx += 1

in_put = open('../Data/index_word.cpkl', 'rb', 1024 * 1024 * 8)
index_word = cPickle.load(in_put)
print 'index_word len: {}'.format(len(index_word))

counter = 0
for top_feature in sorted(feature_map, key=feature_map.get, reverse=False):
    try:
        print top_feature, index_word[top_feature].decode('utf-8'), feature_map[top_feature]
        counter += 1
        if counter == 100: break
    except Exception, e:
        print e