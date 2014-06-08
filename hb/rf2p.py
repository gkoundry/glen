import pandas
import math
import cPickle
import numpy as np
from sklearn.preprocessing import Imputer
from tesla.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.cross_validation import train_test_split,KFold,cross_val_score
from sklearn.linear_model import SGDClassifier,LogisticRegression
from math import log
import sys

def logloss(p,y):
    pn = np.minimum(0.9999,np.maximum(0.0001,p))
    return -np.mean(y*np.log(pn)+(1-y)*np.log(1-pn))

def AMS(s, b):
    """ Approximate Median Significance defined as:
        AMS = sqrt(
                2 { (s + b + b_r) log[1 + (s/(b+b_r))] - s}
              )
    where b_r = 10, b = background, s = signal, log is natural logarithm """

    br = 10.0
    radicand = 2 *( (s+b+br) * math.log (1.0 + s/(b+br)) -s)
    if radicand < 0:
        print 'radicand is negative. Exiting'
        exit()
    else:
        return math.sqrt(radicand)

def maxAMS(pred,wt,y):
    bestsc=0
    bestth=0
    for th in np.linspace(0.4,0.9,50):
        i=0
        sc = 0
        bc = 0
        i=0
        for p in pred:
            if p>th:
                if y[i]==1:
                    sc += wt[i]
                else:
                    bc += wt[i]
            i += 1
        ams = AMS(sc,bc)
        if ams>bestsc:
            bestsc=ams
            bestth=th
    return (bestsc,bestth)

LR=0.1

X=pandas.read_csv("training.csv",na_values='-999.0')
Xv=pandas.read_csv("test.csv",na_values='-999.0')
w=X.pop('Weight')
y=X.pop('Label')
y=(y=='s').astype(int)
eid=Xv['EventId']

imp = Imputer(strategy='most_frequent')
for ws in (2,):
    for mf in (6,):
        for mn in (10,):
            ttr = 0
            for tr in (1000,):
                kf = KFold(X.shape[0], 3, shuffle=True, random_state=1234)
                fo=open('testrfw_%d_%d_%d_%f.csv' % (tr,mf,mn,ws),'w')
                ap=None
                xtrain = X.values
                xtrain = imp.fit_transform(xtrain)
                xtest = Xv.values
                xtest = imp.transform(xtest)
                ytrain = y.values
                wtrain = w.values
                eidtest = eid.values
                #m=LogisticRegression()
                #m=SGDClassifier(alpha=0.000001,loss='log')
                nt = xtrain.shape[0]
                m=RandomForestClassifier(n_estimators=tr,min_samples_leaf=mn,max_features=mf,n_jobs=4)
                m.fit(xtrain,ytrain,sample_weight=(wtrain+ws*1.0)/ws)
                pp=m.predict_proba(xtest)[:,1]
                for i,a in enumerate(eidtest):
                    fo.write('%s,%f\n' % (eidtest[i],pp[i]))
