import datasets
import time
import numpy as np
import scipy.sparse as sp
from wrappers.elastic_net_c import ElasticNetC
from wrappers.glm_c import CGLM
from sklearn.cross_validation import cross_val_score, KFold, train_test_split
from sklearn.metrics import log_loss
from sklearn.linear_model import SGDRegressor, Ridge, LogisticRegression, SGDClassifier, ElasticNet

X = sp.csc_matrix(np.loadtxt('/home/glen/testx177542.out'))
y = np.loadtxt('/home/glen/testy177542.out')
st = time.time()
clf = ElasticNetC(distribution="Tweedie", alpha=0.038778, l1_ratio=0.5, tolerance=0.001, p=1.5)
clf.fit(X, y)
print time.time()-st
