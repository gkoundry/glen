import pandas
import cPickle
import numpy as np
from sklearn.preprocessing import Imputer
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
COL='E'

X=pandas.read_csv("train6%s.csv" % (COL,))
rid=X.pop('id').apply(str)
wt=X.pop('wt')
rest=X.pop('rest')
cvp = ([r'[12467]$',r'[35890]$'],[r'[35890]$',r'[12467]$'])
ls=X.pop('ls')
csls=X.pop('csls')
y=X.pop('y')

imp = Imputer(strategy='most_frequent')
for mf in (3,5,8):
    for mn in (1,5,15):
        ttr = 0
        for tr in (200,400,600):
            scp = 0
            scl = 0
            rsp = 0
            rsl = 0
            tot = 0
            for cv in cvp:
                train=rid.str.contains(cv[0])
                test=rid.str.contains(cv[1])
                xtrain = X.values[train]
                xtrain = imp.fit_transform(xtrain)
                xtest = X.values[test]
                xtest = imp.transform(xtest)
                ytrain = np.logical_and(y.values[train]!=ls.values[train],rest.values[train]==1).astype(int)
                print sum(ytrain.tolist())
                ytest = y.values[test]
                rtest = rest.values[test]
                lstest = ls.values[test]
                m=rgbm.gbm_fit(xtrain,ytrain,nTrain=xtrain.shape[0],bag_fraction=1,n_trees=tr,verbose=False,keep_data=True,n_minobsinnode=mn,distribution="adaboost",interaction_depth=mf,shrinkage=LR) #, w=wtrain[rows]*2.0)
                pp = np.array(rgbm.predict_gbm(m,xtest,n_trees=tr,type="response"))
                print pp.shape
                np.savetxt('test.out',pp,fmt='%f')
                pred=((pp>0.5).astype(int)!=ls.values[test]).astype(int)
                for i,a in enumerate(ytest):
                    p=pred[i]
                    if int(p)==a:
                        scp += 1
                        if rtest[i]==1:
                            rsp += 1
                    if lstest[i]==a:
                        scl += 1
                        if rtest[i]==1:
                            rsl += 1
                    tot += 1
            print 'tr%d mf%d mn%d scp %d scl %d rsp %d rsl %d tot %d' % (tr,mf,mn,scp,scl,rsp,rsl,tot)
