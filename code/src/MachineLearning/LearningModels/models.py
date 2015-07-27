__author__ = 'hanxuan'

from sklearn import linear_model
from sklearn.svm import SVC, SVR, LinearSVC, LinearSVR, NuSVC, NuSVR
from SparseMatrixReader import SparseMatrixReader
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import classification_report
from sklearn.neural_network import BernoulliRBM
from sklearn.pipeline import Pipeline

import numpy as np
import matplotlib.pyplot as plt
from sklearn.learning_curve import learning_curve

def plot_learning_curve(estimator, title, X, y, ylim=None, cv=None,
                        n_jobs=1, train_sizes=np.linspace(.1, 1.0, 5)):
    train_sizes, train_scores, test_scores = learning_curve(estimator, X, y, cv=cv, n_jobs=n_jobs, train_sizes=train_sizes)
    train_scores_mean = np.mean(train_scores, axis=1)
    train_scores_std = np.std(train_scores, axis=1)
    test_scores_mean = np.mean(test_scores, axis=1)
    test_scores_std = np.std(test_scores, axis=1)

    plt.figure()
    plt.title(title)
    if ylim is not None:
        plt.ylim(*ylim)
    plt.xlabel("Training examples")
    plt.ylabel("Score")
    plt.grid()

    plt.fill_between(train_sizes, test_scores_mean - test_scores_std, test_scores_mean + test_scores_std, alpha=0.1, color="g")
    plt.fill_between(train_sizes, train_scores_mean - train_scores_std, train_scores_mean + train_scores_std, alpha=0.1, color="r")
    plt.plot(train_sizes, train_scores_mean, 'o-', color="r", label="Training score")
    plt.plot(train_sizes, test_scores_mean, 'o-', color="g", label="Cross-validation score")

    plt.legend(loc="best")
    return plt



training_file_path = '../Data/ap89_training.txt'
testing_file_path = '../Data/ap89_testing.txt'

smr_train = SparseMatrixReader(training_file_path)
smr_test = SparseMatrixReader(testing_file_path)

logreg = linear_model.LogisticRegression(max_iter=5000, solver='liblinear', verbose=True)
print 'LogisticRegression config:'
print logreg.get_params()
logreg.fit(smr_train.feature_matrix, smr_train.labels)
logreg_score_train = logreg.score(smr_train.feature_matrix, smr_train.labels)
print 'LogisticRegression precision train: {}'.format(logreg_score_train)
logreg_score_test = logreg.score(smr_test.feature_matrix, smr_test.labels)
print 'LogisticRegression precision test: {}'.format(logreg_score_test)
print 'RAW LogisticRegression performance:'
print classification_report(smr_test.labels, logreg.predict(smr_test.feature_matrix))
plot_learning_curve(logreg, 'LogisticRegression Curve', smr_train.feature_matrix, smr_train.labels, n_jobs=4)
plt.show()
print ''


logistic = linear_model.LogisticRegression()
rbm = BernoulliRBM(random_state=0, verbose=True)
classifier = Pipeline(steps=[('rbm', rbm), ('logistic', logistic)])
rbm.learning_rate = 0.06
rbm.n_iter = 20
rbm.n_components = 100
logistic.C = 6000.0
classifier.fit(smr_train.feature_matrix, smr_train.labels)
rbm_logreg_score_train = classifier.score(smr_train.feature_matrix, smr_train.labels)
print 'RBM_LogisticRegression precision train: {}'.format(rbm_logreg_score_train)
rbm_logreg_score_test = classifier.score(smr_test.feature_matrix, smr_test.labels)
print 'RBM_LogisticRegression precision test: {}'.format(rbm_logreg_score_test)
print("TRAIN: Logistic regression using RBM features:\n%s\n" % (classification_report(smr_train.labels, classifier.predict(smr_train.feature_matrix))))
print("TEST: Logistic regression using RBM features:\n%s\n" % (classification_report(smr_test.labels, classifier.predict(smr_test.feature_matrix))))
# plot_learning_curve(classifier, 'classifier Curve', smr_train.feature_matrix, smr_train.labels, n_jobs=4)

logregCV = linear_model.LogisticRegressionCV(max_iter=5000, solver='liblinear')
print 'LogisticRegressionCV config:'
print logregCV.get_params()
logregCV.fit(smr_train.feature_matrix, smr_train.labels)
logregCV_score_train = logregCV.score(smr_train.feature_matrix, smr_train.labels)
print 'LogisticRegressionCV precision train: {}'.format(logregCV_score_train)
logregCV_score_test = logregCV.score(smr_test.feature_matrix, smr_test.labels)
print 'LogisticRegressionCV precision test: {}'.format(logregCV_score_test)
print 'RAW LogisticRegressionCV performance:'
print classification_report(smr_test.labels, logregCV.predict(smr_test.feature_matrix))
# plot_learning_curve(logregCV, 'logregCV Curve', smr_train.feature_matrix, smr_train.labels, n_jobs=4)
print ''

svc = SVC(gamma=0.001, kernel='linear')
print 'SVC config:'
print svc.get_params()
svc.fit(smr_train.feature_matrix, smr_train.labels)
svc_score_train = svc.score(smr_train.feature_matrix, smr_train.labels)
print 'SVC precision train: {}'.format(svc_score_train)
svc_score_test = svc.score(smr_test.feature_matrix, smr_test.labels)
print 'SVC precision test: {}'.format(svc_score_test)
# plot_learning_curve(svc, 'SVC Curve', smr_train.feature_matrix, smr_train.labels, n_jobs=4)
print ''

svr = SVR()
print 'SVR config:'
print svr.get_params()
svr.fit(smr_train.feature_matrix, smr_train.labels)
svr_score_train = svr.score(smr_train.feature_matrix, smr_train.labels)
print 'SVR precision train: {}'.format(svr_score_train)
svr_score_test = svr.score(smr_test.feature_matrix, smr_test.labels)
print 'SVR precision test: {}'.format(svr_score_test)
# plot_learning_curve(svr, 'SVR Curve', smr_train.feature_matrix, smr_train.labels, n_jobs=4)
print ''

lsvc = LinearSVC()
print 'LinearSVC config:'
print lsvc.get_params()
lsvc.fit(smr_train.feature_matrix, smr_train.labels)
lsvc_score_train = lsvc.score(smr_train.feature_matrix, smr_train.labels)
print 'LinearSVC precision train: {}'.format(lsvc_score_train)
lsvc_score_test = lsvc.score(smr_test.feature_matrix, smr_test.labels)
print 'LinearSVC precision test: {}'.format(lsvc_score_test)
print ''

lsvr = LinearSVR()
print 'LinearSVR config:'
print svc.get_params()
lsvr.fit(smr_train.feature_matrix, smr_train.labels)
lsvr_score_train = svc.score(smr_train.feature_matrix, smr_train.labels)
print 'LinearSVR precision train: {}'.format(lsvr_score_train)
lsvr_score_test = lsvr.score(smr_test.feature_matrix, smr_test.labels)
print 'LinearSVR precision test: {}'.format(lsvr_score_test)
print ''

nusvc = NuSVC()
print 'NuSVC config:'
print nusvc.get_params()
nusvc.fit(smr_train.feature_matrix, smr_train.labels)
nusvc_score_train = nusvc.score(smr_train.feature_matrix, smr_train.labels)
print 'NuSVC precision train: {}'.format(nusvc_score_train)
nusvc_score_test = nusvc.score(smr_test.feature_matrix, smr_test.labels)
print 'NuSVC precision test: {}'.format(nusvc_score_test)
print ''

nusvr = NuSVR()
print 'NuSVR config:'
print nusvr.get_params()
nusvr.fit(smr_train.feature_matrix, smr_train.labels)
nusvr_score_train = svc.score(smr_train.feature_matrix, smr_train.labels)
print 'NuSVR precision train: {}'.format(nusvr_score_train)
nusvr_score_test = nusvr.score(smr_test.feature_matrix, smr_test.labels)
print 'NuSVR precision test: {}'.format(nusvr_score_test)
print ''


dtc = DecisionTreeClassifier()
print 'DecisionTreeClassifier config:'
print dtc.get_params()
dtc.fit(smr_train.feature_matrix, smr_train.labels)
dtc_score_train = dtc.score(smr_train.feature_matrix, smr_train.labels)
print 'DecisionTreeClassifier precision train: {}'.format(dtc_score_train)
dtc_score_test = dtc.score(smr_test.feature_matrix, smr_test.labels)
print 'DecisionTreeClassifier precision test: {}'.format(dtc_score_test)
print classification_report(smr_test.labels, dtc.predict(smr_test.feature_matrix))
print ''
