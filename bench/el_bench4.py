import datasets
from wrappers.elastic_net_c import ElasticNetC
import time
import sys
import math
import numpy as np
from wrappers.glmnet import GlmnetWrapper
from wrappers.glm_c import CGLM
from sklearn.cross_validation import cross_val_score, KFold
from sklearn.metrics import make_scorer, mean_absolute_error
from sklearn.linear_model import SGDRegressor, Ridge, LogisticRegression, SGDClassifier, ElasticNet

cn=0
ag=0
lmg=0

def rmsle(act, pred):
    global cn
    global ag
    global lmg
    #import random
    #np.savetxt('temp'+cn+'_'+ag+'_'+lmg+'_'+str(random.randint(0,999999))+'.out',np.column_stack((act,pred)),fmt='%.5f')
    return np.log((act-pred)**2).mean()

def psdev(act, pred):
    sc = 0
    for i in range(act.shape[0]):
        if act[i]==0:
            sc += 2 * pred[i]
        else:
            if pred[i]<=0:
                sc += 2 * (act[i] * math.log(act[i]/0.1) - (act[i] - pred[i]))
            else:
                sc += 2 * (act[i] * math.log(act[i]/pred[i]) - (act[i] - pred[i]))
    return sc/act.shape[0]

RMSLE = make_scorer(rmsle, greater_is_better=False)
PSDEV = make_scorer(psdev, greater_is_better=False)

#for ds in datasets.get_datasets(rtype='Positive'): #,name='census_1990_small'):
for ds in datasets.get_datasets(name='census_2012h_small'):
    #if 'census' in ds['name']: continue
    X, y = datasets.get_data(ds,standardize=False)
    kf = KFold(X.shape[0], 2, shuffle=True, random_state=1234)
    for a in (0.1, 0.3, 0.6, 0.9):
        for lm in (1, 0.1, 0.01):
            clf1 = CGLM(distribution='Poisson',trace=False)
            clf2 = Ridge(alpha=lm)
            clf3 = ElasticNetC(distribution='Poisson', alpha=lm, l1_ratio=a, tolerance=0.001)
            #clf3t = ElasticNetC(distribution='Tweedie', alpha=lm, l1_ratio=a, tolerance=0.001,p=1.5)
            #clf3g = ElasticNetC(distribution='Gamma', alpha=lm, l1_ratio=a, tolerance=0.001)
            clf4 = GlmnetWrapper(**{'family': 'gaussian', 'alpha': a, 'lambda': lm, 'maxit': 300})
            #clf4 = GlmnetWrapper(**{'family': 'poisson', 'alpha': a, 'lambda': lm, 'maxit': 300})
            score_func = PSDEV #'roc_auc'
            for clf in (clf1, clf2, clf3, clf4):
            #for clf in (clf1, clf2, clf3, clf3t, clf3g, clf4):
                if clf != clf1 or (a == 0.1 and lm == 10):
                    cn=clf.__class__.__name__
                    ag = str(a)
                    lmg=str(lm)
                    st = time.time()
                    print '%-20s %20s a %3.1f lm %8.4f sc %9.4f tm %5.2f' % \
                          (ds['name'], clf.__class__.__name__, a, lm,
                           cross_val_score(clf, X, y, cv=kf, scoring=score_func, n_jobs=4).mean(), time.time()-st)
                    sys.stdout.flush()
