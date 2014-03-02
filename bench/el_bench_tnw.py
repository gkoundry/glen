import datasets
import time
import numpy as np
from wrappers.elastic_net_c import ElasticNetC
from wrappers.glm_c import CGLM
from sklearn.cross_validation import cross_val_score, KFold, train_test_split
from sklearn.metrics import log_loss
from sklearn.linear_model import SGDRegressor, Ridge, LogisticRegression, SGDClassifier, ElasticNet

ds = datasets.get_datasets(name="trainingDataWithoutNegativeWeights")[0]
X, y = datasets.get_data(ds,standardize=False)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.75, random_state=42)
#kf = KFold(X.shape[0], 2, shuffle=True, random_state=1234)
#score_func="log_loss"

#0.010000 log 0.750000 0.251992
#for e in (0.01,):
#    for l in ('log',):
#        for a in (4,2,1,0.75,0.5):
#            clf = SGDClassifier(eta0=e,loss=l,alpha=a)
#            clf.fit(X_train, y_train)
#            p=clf.predict_proba(X_test)
#            print '%f %s %f %f' % (e,l,a,log_loss(y_test, p)) #np.column_stack((1-p,p))))

#clf = CGLM(distribution="Bernoulli")
#clf.fit(X_train, y_train)
#p=clf.predict(X_test)
#print log_loss(y_test, np.column_stack((1-p,p)))
#
#sp 0.295693095075 t 3420.74344611
for a in (0.01,):
    st = time.time()
    clf = ElasticNetC(distribution="Bernoulli", alpha=a, l1_ratio=0.1, tolerance=0.001)
    print X_train.shape
    clf.fit(X_train, y_train)
    p=clf.predict(X_test)
    print str(log_loss(y_test, np.column_stack((1-p,p))))+' t '+str(time.time()-st)
#
#print cross_val_score(clf, X, y, cv=kf, scoring=score_func, n_jobs=4).mean()
#clf = ElasticNetC(distribution="Bernoulli", alpha=0.01, l1_ratio=0.1, tolerance=0.001)
#print cross_val_score(clf, X, y, cv=kf, scoring=score_func, n_jobs=4).mean()
