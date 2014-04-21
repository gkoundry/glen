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

X=pandas.read_csv("train9all.csv")
rid=X.pop('id').apply(str)
last=X.pop('last')
y=X.pop('ans')

imp = Imputer(strategy='most_frequent')
#for mf in (3,7,):
for mf in (5,):
    #for mn in (1,20,100,):
    for mn in (5,):
        ttr = 0
        #for tr in (5,100,200,400,):
        for tr in (100,):
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
                lasttest = last.values[test]
                idtest = rid.values[test].astype(float)
                m=rgbm.gbm_fit(xtrain,ytrain,nTrain=xtrain.shape[0],bag_fraction=1,n_trees=tr,verbose=False,keep_data=False,n_minobsinnode=mn,distribution='multinomial',interaction_depth=mf,shrinkage=LR) #, w=wtrain[rows]*2.0)
                ppp=rgbm.predict_gbm(m,xtest,n_trees=tr,type="response")
                pp = np.array(ppp)
                levels = np.array(ppp.names[1]).astype(int)
                #print pp.shape
                pred=np.argmax(pp,axis=1)
                for i,a in enumerate(ytest):
                    if int(lasttest[i])==int(a):
                        scl += 1
                    if int(levels[pred[i]])==int(a):
                        scp += 1
                    tot += 1
            print 'tr%d mf%d mn%d scp %d scl %d tot %d' % (tr,mf,mn,scp,scl,tot)
            sys.stdout.flush()
