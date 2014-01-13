import datasets
import time
import numpy as np
from sklearn.cross_validation import cross_val_score
from sklearn.linear_model import SGDRegressor, Ridge, LogisticRegression, SGDClassifier
from sklearn.metrics import log_loss, mean_absolute_error, mean_squared_error

ds = datasets.get_datasets(name='kickcars_small')
X,y = datasets.get_data(ds)

def LogLoss(clf, X, y):
    p = clf.predict_proba(X)
    if len(p.shape) == 1 or p.shape[1] == 1:
        p = np.column_stack((1-p, p))
    return log_loss(y, p)

for lm in (1000, 1, 0.1, 0.01, 0.001):
    for a in (0.1, 0.3, 0.6):
        st=time.time()
        clf = SGDClassifier(alpha=lm, l1_ratio=a, loss='log', eta0=0.001, penalty='elasticnet')
        print '%-20s a %3.1f lm %8.4f sc %9.4f tm %5.2f' % (clf.__class__.__name__, a, lm, np.mean(cross_val_score(clf, X, y, cv=5, scoring=LogLoss)), time.time()-st)
