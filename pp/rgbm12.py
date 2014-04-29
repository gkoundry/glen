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
if len(sys.argv)>1:
    COL1=sys.argv[1]
else:
    COL1='F'
LEVELS={
    'A': ('0','1','2'),
    'B': ('0','1'),
    'C': ('1','2','3','4'),
    'D': ('1','2','3'),
    'E': ('0','1'),
    'F': ('0','1','2','3'),
    'G': ('1','2','3','4'),
}

X=pandas.read_csv("train12%s.csv" % (COL1,))
rid=X.pop('id').apply(str)
ls=X.pop('ls')
rest=X.pop('rest')
y=X.pop('y')
last=X.pop('last')
ans=X.pop('ans')

fo=open('pred'+COL1+'.csv','w')
imp = Imputer(strategy='most_frequent')
for mf in (5,9,):
#for mf in (5,):
    #for mn in (1,20,100,):
    for mn in (1,10,50):
        ttr = 0
        #for tr in (100,200,400,):
        for tr in (100,200,400):
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
                m=rgbm.gbm_fit(xtrain,ytrain,nTrain=xtrain.shape[0],bag_fraction=1,n_trees=tr,verbose=False,keep_data=False,n_minobsinnode=mn,distribution='multinomial',interaction_depth=mf,shrinkage=LR) #, w=wtrain[rows]*2.0)
                ppp=rgbm.predict_gbm(m,xtest,n_trees=tr,type="response")
                pp = np.array(ppp)
                levels = np.array(ppp.names[1]).astype(int)
                #print pp.shape
                pred=np.argmax(pp,axis=1)
                for i,a in enumerate(ytest):
                    #print '%s %07d %07d %d %s %s' % (idtest[i],anstest[i],lasttest[i],int(levels[pred[i]]),int(levels[pred[i]])==int(a) and rtest[i]==1,lstest[i]==int(a) and rtest[i]==1)
                    if int(lstest[i])==int(a):
                        scl += 1
                        if rtest[i]==1:
                            rsl += 1
                    fo.write("%07d,%02d\n" % (idtest[i],levels[pred[i]]))
                    aa = '%07d' % anstest[i]
                    ab = '%07d' % lasttest[i]
                    p1 = '%02d' % int(levels[pred[i]])
                    ab=list(ab)
                    ab[ord(COL1)-65] = p1[0]
                    ab=''.join(ab)
                    #print '%s %s %s %d' % ( idtest[i],aa,ab, int(int(levels[pred[i]])==int(a) and rtest[i]==1))
                    if int(levels[pred[i]])==int(a):
                        scp += 1
                        if rtest[i]==1:
                            rsp += 1
                    tot += 1
            print '%s tr%d mf%d mn%d scp %d scl %d rsp %d rsl %d tot %d' % (COL1,tr,mf,mn,scp,scl,rsp,rsl,tot)
            sys.stdout.flush()
