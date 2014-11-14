import pandas
import math
import cPickle
import numpy as np
from sklearn.preprocessing import Imputer
from GLM import GLM
from sklearn.cross_validation import train_test_split,KFold,cross_val_score
from sklearn.linear_model import SGDClassifier,LogisticRegression
from math import log
from ams import maxAMS
import sys

def wrmse(pred,act,weight=None):
    """
        RMSE = Root Mean Squared Error = sqrt( sum( (act - pred)**2 ) )
    """
    if len(pred.shape)>1: pred = pred.ravel()
    d = act - pred
    #if weight is not None:
    #    d = d*weight
    #mse = np.power(d,2).mean()
    sd=np.power(d,2)
    if weight is not None:
        if weight.sum()==0:
            return 0
        sd = sd*weight/weight.mean()
    mse = sd.mean()
    return np.sqrt(mse)

X=pandas.read_csv("merge2.csv")
w=X.pop('Weight')
y=X.pop('Label')
id=X.pop('EventId')
cols = ['ALL']+list(X.columns)
#for c in cols:
for c in ['ALL']:
    X=pandas.read_csv("merge2.csv")
    w=X.pop('Weight')
    y=X.pop('Label')
    id=X.pop('EventId')
    if c!='ALL':
        X.pop(c)
    sys.stdout.write('%s ' % c)
    #cols = X.columns
    #for c in cols:
    ##    X[c+'_sqr'] = X[c] * X[c]
    #    X[c] = np.maximum(0.00001,np.minimum(0.99999,X[c].values))
    #    X[c+'_lg'] = np.log(X[c].values) - np.log(1-X[c].values)
    #X = np.maximum(0.00001,np.minimum(0.99999,X.values))
    X=X.values

    kf = KFold(X.shape[0], 5, shuffle=True, random_state=1234)
    bm = 1
    ba = 0
    s1 = 0.7
    s2 = 0.7
    s3 = 0.7
    s4 = 7
    for lg in (False,):
        for s1 in (0.05,0.1,0.2):
            for s2 in (1.6,2,2.4):
                for s3 in (0.1,0.2,0.4):
                    for s4 in (3.5,4,4.5):
                        predv = np.zeros(X.shape[0])
                        predt = np.zeros(X.shape[0])
                        wt = np.zeros(X.shape[0])
                        wv = np.zeros(X.shape[0])
                        wxt = np.zeros(X.shape[0])
                        wxv = np.zeros(X.shape[0])
                        yt = np.zeros(X.shape[0])
                        yv = np.zeros(X.shape[0])
                        ok = True
                        for train,test in kf:
                            if lg:
                                xtrain = np.log(X[train]) - np.log(1-X[train])
                                xtest = np.log(X[test]) - np.log(1-X[test])
                            else:
                                xtrain = X[train]
                                xtest = X[test]
                            ytrain = y.values[train]
                            ytest = y.values[test]
                            wtrain = w.values[train]
                            wtrainx = w.values[train].copy()
                            mask_st1 = np.abs(wtrainx - 0.00150187015894) < 0.0000001
                            mask_st2 = np.abs(wtrainx - 0.001502704831) < 0.0000001
                            mask_st3 = np.abs(wtrainx - 0.002653311337) < 0.0000001
                            mask_st4 = np.abs(wtrainx - 0.018636116672) < 0.0000001
                            wtrainx[mask_st1] = s1
                            wtrainx[mask_st2] = s2
                            wtrainx[mask_st3] = s3
                            wtrainx[mask_st4] = s4
                            wtrainx[ytrain==0] = np.sqrt(wtrainx[ytrain==0]) * bm + ba
                            wtestx = w.values[test].copy()
                            mask_sv1 = np.abs(wtestx - 0.00150187015894) < 0.0000001
                            mask_sv2 = np.abs(wtestx - 0.001502704831) < 0.0000001
                            mask_sv3 = np.abs(wtestx - 0.002653311337) < 0.0000001
                            mask_sv4 = np.abs(wtestx - 0.018636116672) < 0.0000001
                            wtestx[mask_sv1] = s1
                            wtestx[mask_sv2] = s2
                            wtestx[mask_sv3] = s3
                            wtestx[mask_sv4] = s4
                            wtestx[ytest==0] = np.sqrt(wtestx[ytest==0]) * bm + ba
                            wtest = w.values[test]
                            if np.any(wtrainx<0):
                                ok = False
                                break
                            m=GLM()
                            m.fit(np.ascontiguousarray(xtrain).astype(float),ytrain.astype(float),weights=wtrainx,distribution='Gaussian')
                            #print m.coef_
                            pt=m.predict(np.ascontiguousarray(xtrain).astype(float))
                            pv=m.predict(np.ascontiguousarray(xtest).astype(float))
                            predt[train] += pt
                            predv[test] += pv
                            wt[train] = wtrain
                            wv[test] = wtest
                            wxt[train] = wtrainx
                            wxv[test] = wtestx
                            yt[train] = ytrain
                            yv[test] = ytest
                        if ok:
                            print '%s %s %s %s %s %s %s %s %s %s %s' % (lg,s1,s2,s3,s4,bm,ba,wrmse(predv,yv,wxv),wrmse(predt,yt,wxt),maxAMS(predv,yv,wv,1)[0],maxAMS(predt/2,yt,wt,1)[0])
                            sys.stdout.flush()
