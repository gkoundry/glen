import pandas
import cPickle
import numpy as np
from sklearn.preprocessing import Imputer
from sklearn.cross_validation import train_test_split,KFold,cross_val_score
from math import log
import sys
import rpy2.robjects as robjects
import rpy2.robjects.numpy2ri
rpy2.robjects.numpy2ri.activate()
from rpy2.robjects.numpy2ri import numpy2ri
robjects.conversion.py2ri = numpy2ri
from rpy2.robjects.packages import importr
rgbm = importr("gbm")

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

X=pandas.read_csv("train9sc.csv")
rid=X.pop('id').apply(str)
ls=X.pop('ls')
rest=X.pop('rest')
yy=X.pop('y')
y=X.pop('yy')
last=X.pop('last')
ans=X.pop('ans')

imp = Imputer(strategy='most_frequent')
for mf in (5,8,):
#for mf in (5,):
    #for mn in (1,20,100,):
    for mn in (10,30,60):
        ttr = 0
        #for tr in (100,200,400,):
        for tr in (200,300,400):
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
                ytrain = y.values[train]
                ytest = y.values[test]
                rtest = rest.values[test]
                lstest = ls.values[test]
                lasttest = last.values[test]
                anstest = ans.values[test]
                idtest = rid.values[test].astype(float)
                m=rgbm.gbm_fit(xtrain,ytrain,nTrain=xtrain.shape[0],bag_fraction=1,n_trees=tr,verbose=False,keep_data=False,n_minobsinnode=mn,distribution='bernoulli',interaction_depth=mf,shrinkage=LR) #, w=wtrain[rows]*2.0)
                ppp=rgbm.predict_gbm(m,xtest,n_trees=tr,type="response")
                pp = np.array(ppp)
                for i,a in enumerate(ytest):
                    pred = int(pp[i]>0.5)
                    if pred==a:
                        scl+=1
                    tot += 1
            print 'tr%d mf%d mn%d scp %d scl %d rsp %d rsl %d tot %d' % (tr,mf,mn,scp,scl,rsp,rsl,tot)
            sys.stdout.flush()
