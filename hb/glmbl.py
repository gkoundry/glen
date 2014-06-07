import pandas
import math
import cPickle
import numpy as np
from sklearn.preprocessing import Imputer
from GLM import GLM
from sklearn.cross_validation import train_test_split,KFold,cross_val_score
from sklearn.linear_model import SGDClassifier,LogisticRegression
from math import log
import sys

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

LR=0.1

X=pandas.read_csv("vote.csv",na_values='-999.0')
w=X.pop('wt')
y=X.pop('y')

for th in (0.66,0.67,0.68,0.69):
    #fo=open('predrgbm_%d_%f_%d_na.csv' % (tr,LR,mn),'w')
    scs = 0
    scb = 0
    kf = KFold(X.shape[0], 2, shuffle=True, random_state=1234)
    for train,test in kf:
        xtrain = X.values[train]
#                xtrain = imp.fit_transform(xtrain)
        xtest = X.values[test]
#                xtest = imp.transform(xtest)
        ytrain = y.values[train]
        ytest = y.values[test]
        wtrain = w.values[train]
        wtest = w.values[test]
        #m=LogisticRegression()
        #m=SGDClassifier(alpha=0.000001,loss='log')
        nt = xtrain.shape[0]
        #xtrain=robjects.r['data.frame'](xtrain)
        m=GLM()
        m.fit(np.ascontiguousarray(xtrain).astype(float),ytrain.astype(float))
        pp=m.predict(np.ascontiguousarray(xtrain).astype(float))
        for i,a in enumerate(ytrain):
            #fo.write('%s,%f\n' % (eidtest[i],pp[i]))
            #if pp[i]>th:
            if xtrain[i][22]>th:
                if a==1:
                    scs += wtrain[i]
                else:
                    scb += wtrain[i]
    print 'th%f %f %f %f' % (th,scs,scb,AMS(scs,scb))
    sys.stdout.flush()
