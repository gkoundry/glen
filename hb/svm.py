import pandas
import math
import cPickle
import numpy as np
from sklearn.preprocessing import Imputer
from tesla.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.cross_validation import train_test_split,KFold,cross_val_score
from sklearn.svm import SVC
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
w=X.pop('Weight')
y=X.pop('Label')
y=(y=='s').astype(int)
eid=X['EventId']

imp = Imputer(strategy='most_frequent')
for C in (1,2,5,):
    kf = KFold(X.shape[0], 3, shuffle=True, random_state=1234)
    fo=open('trainsvmw_%f.csv' % (C,),'w')
    ap=None
    for train,test in kf:
        xtrain = X.values[train]
        xtrain = imp.fit_transform(xtrain)
        xtest = X.values[test]
        xtest = imp.transform(xtest)
        ytrain = y.values[train]
        ytest = y.values[test]
        wtrain = w.values[train]
        wtest = w.values[test]
        eidtest = eid.values[test]
        #m=LogisticRegression()
        #m=SGDClassifier(alpha=0.000001,loss='log')
        nt = xtrain.shape[0]
        m=SVC(C=C,probability=True,random_state=1234)
        m.fit(xtrain,ytrain,wtrain)
        pp=m.predict_proba(xtest)[:,1]
        for i,a in enumerate(ytest):
            fo.write('%s,%f\n' % (eidtest[i],pp[i]))
        if ap is None:
            ap=pp
            ay=ytest
            aw=wtest
        else:
            ap=np.concatenate((ap,pp))
            ay=np.concatenate((ay,ytest))
            aw=np.concatenate((aw,wtest))
    print 'C%f %s %f' % (C,maxAMS(ap,aw,ay),logloss(ap,ay))
    sys.stdout.flush()
