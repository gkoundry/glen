import datasets
from wrappers.elastic_net_c import ElasticNetC
import time
from wrappers.glmnet import GlmnetWrapper
from wrappers.zeroinfl import ZeroInflWrapper
from wrappers.glm_c import CGLM
from sklearn.cross_validation import cross_val_score, KFold
from sklearn.metrics import make_scorer, mean_absolute_error
from sklearn.linear_model import SGDRegressor, Ridge, LogisticRegression, SGDClassifier, ElasticNet

MAD = make_scorer(mean_absolute_error, greater_is_better=False)
score_func='r2'

for ds in datasets.get_datasets(name='mets_short'):
    X, y = datasets.get_data(ds)
    kf = KFold(X.shape[0], 15, shuffle=True, random_state=1234)
    for a in (0.1, 0.5, 1.0, 1.5):
        clf1 = Ridge(alpha=a)
        clf2 = CGLM(distribution='Poisson',trace=False)
        clf3 = ZeroInflWrapper()
        for clf in (clf1,clf2,clf3):
            if a!=0.1 and clf!=clf1:
                continue
            st = time.time()
            print '%-20s %20s a %3.1f sc %9.4f tm %5.2f' % \
                  (ds['name'], clf.__class__.__name__, a,
                   cross_val_score(clf, X, y, cv=kf, scoring=score_func, n_jobs=3).mean(), time.time()-st)
