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

def RMSE(p,y):
    return math.sqrt(np.mean((y-p)**2))

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

X=pandas.read_csv("training_imp.csv",na_values='-999.0')
w=X.pop('Weight')
y=X.pop('Label')
w[y==1] = w[y==1] * 100
w[y==0] = w[y==0] * -1
eid=X['EventId']

imp = Imputer(strategy='most_frequent')
for mf in (16,):
    for mn in (10,):
        ttr = 0
        for tr in (1000,):
            kf = KFold(X.shape[0], 5, shuffle=True, random_state=1234)
            fo=open('trainrfg_%d_%d_%d.csv' % (tr,mf,mn),'w')
            ap=None
            for train,test in kf:
                xtrain = X.values[train]
                xtrain = imp.fit_transform(xtrain)
                xtest = X.values[test]
                xtest = imp.transform(xtest)
                #ytrain = y.values[train]
                ytest = y.values[test]
                wtrain = w.values[train]
                wtest = w.values[test]
                eidtest = eid.values[test]
                #m=LogisticRegression()
                #m=SGDClassifier(alpha=0.000001,loss='log')
                nt = xtrain.shape[0]
                m=RandomForestRegressor(n_estimators=tr,min_samples_leaf=mn,max_features=mf,n_jobs=4)
                m.fit(xtrain,wtrain)
                pp=m.predict(xtest)
                for i,a in enumerate(wtest):
                    fo.write('%s,%f\n' % (eidtest[i],pp[i]))
                if ap is None:
                    ap=pp
                    ay=ytest
                    aw=wtest
                else:
                    ap=np.concatenate((ap,pp))
                    ay=np.concatenate((ay,ytest))
                    aw=np.concatenate((aw,wtest))
            print 'tr%d mn%d mf%d %s %f' % (tr,mn,mf,maxAMS(ap,aw,ay),RMSE(ap,aw))
            sys.stdout.flush()
