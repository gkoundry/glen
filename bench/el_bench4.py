import datasets
from wrappers.elastic_net_c import ElasticNetC
import time
import numpy as np
from wrappers.glmnet import GlmnetWrapper
from wrappers.glm_c import CGLM
from sklearn.cross_validation import cross_val_score, KFold
from sklearn.metrics import make_scorer, mean_absolute_error

def rmsle(act, pred):
    return np.log((act-pred)**2).mean()

RMSLE = make_scorer(rmsle, greater_is_better=False)

for ds in datasets.get_datasets(rtype='Positive'):
    X, y = datasets.get_data(ds)
    kf = KFold(X.shape[0], 5, shuffle=True, random_state=1234)
    for a in (0.1, 0.3, 0.6, 0.9):
        for lm in (1, 0.1, 0.01, 0.001):
            clf1 = CGLM(distribution='Poisson',trace=False)
            clf2 = ElasticNetC(distribution='Poisson', alpha=lm, l1_ratio=a, tolerance=0.001)
            clf3 = GlmnetWrapper(**{'family': 'poisson', 'alpha': a, 'lambda': lm, 'maxit': 300})
            score_func = RMSLE
            for clf in (clf1, clf2, clf3):
                if clf != clf1 or (a == 0.1 and lm == 1):
                    st = time.time()
                    print '%-20s %20s a %3.1f lm %8.4f sc %9.4f tm %5.2f' % \
                          (ds['name'], clf.__class__.__name__, a, lm,
                           cross_val_score(clf, X, y, cv=kf, scoring=score_func, n_jobs=3).mean(), time.time()-st)
