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
    X, y = datasets.get_data(ds,standardize=False)
    kf = KFold(X.shape[0], 2, shuffle=True, random_state=1234)
    clf3 = ElasticNetC(distribution='Poisson', l1_ratio=0.5, tolerance=0.001, alpha_count=10)
    clf3.fit(X,y)
    for i in clf3.coef_:
        print i
