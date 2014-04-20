import pandas
import cPickle
import sys
import numpy as np
from sklearn.preprocessing import Imputer
from sklearn.cross_validation import train_test_split,KFold,cross_val_score
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from math import log

LR=0.03
LEVELS={
    'A': ('0','1','2'),
    'B': ('0','1'),
    'C': ('1','2','3','4'),
    'D': ('1','2','3'),
    'E': ('0','1'),
    'F': ('0','1','2','3'),
    'G': ('1','2','3','4'),
}

X=pandas.read_csv("train9all.csv")
rid=X.pop('id').apply(str)
last=X.pop('last')
y=X[['yA','yB','yC','yD','yE','yF','yG']]
yy=X[['yE','yG']]
X=X.drop(['yA','yB','yC','yD','yE','yF','yG'],axis=1)

imp = Imputer(strategy='most_frequent')
for mf in (3,7,12,20):
#for mf in (10,):
    for mn in (1,20,100,):
    #for mn in (5,):
        ttr = 0
        #for tr in (5,100,200,400,):
        for tr in (200,):
            scp = 0
            scl = 0
            rsp = 0
            rsl = 0
            tot = 0
            kf = KFold(X.shape[0], 3, shuffle=True, random_state=1234)
            for train,test in kf:
                xtrain = X.values[train]
                xtrain = imp.fit_transform(xtrain)
                xtest = X.values[test]
                xtest = imp.transform(xtest)
                ytrain = yy.values[train]
                ytest = y.values[test]
                lasttest = last.values[test]
                idtest = rid.values[test].astype(float)
                m=RandomForestClassifier(n_estimators=tr,min_samples_leaf=mn,max_features=mf,n_jobs=6)
                m.fit(xtrain,ytrain)
                p=m.predict(xtest)
                for i,a in enumerate(ytest):
                    ans=''.join([str(int(j)) for j in a.tolist()])
                    ls=('%07d' % (np.asscalar(lasttest[int(i)]),))
                    pred=ls[:4]+str(int(p[i][0]))+ls[5]+str(int(p[i][1]))
                    #print '%s %s %s' % (ans,pred,ls)
                    if ls==ans:
                        scl += 1
                    if pred==ans:
                        scp += 1
                    tot += 1
            print 'tr%d mf%d mn%d scp %d scl %d tot %d' % (tr,mf,mn,scp,scl,tot)
            sys.stdout.flush()
