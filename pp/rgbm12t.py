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

#A tr200 mf9 mn20 scp 85983 scl 85265 rsp 52406 rsl 52638 tot 97009
#B tr200 mf9 mn20 scp 86257 scl 86221 rsp 52638 rsl 52638 tot 97009
#C tr200 mf9 mn20 scp 85486 scl 84656 rsp 52514 rsl 52638 tot 97009
#D tr200 mf9 mn20 scp 88317 scl 87868 rsp 52530 rsl 52638 tot 97009
#E tr200 mf9 mn20 scp 86560 scl 86404 rsp 52628 rsl 52638 tot 97009
#F tr200 mf9 mn20 scp 85436 scl 84974 rsp 52491 rsl 52638 tot 97009
#G tr200 mf9 mn20 scp 78549 scl 77690 rsp 52855 rsl 52638 tot 97009

#wa
#A tr200 mf9 mn20 scp 85992 scl 85265 rsp 52417 rsl 52638 tot 97009
#B tr200 mf9 mn20 scp 86256 scl 86221 rsp 52638 rsl 52638 tot 97009
#C tr200 mf9 mn20 scp 85501 scl 84656 rsp 52517 rsl 52638 tot 97009
#D tr200 mf9 mn20 scp 88334 scl 87868 rsp 52540 rsl 52638 tot 97009
#F tr200 mf9 mn20 scp 85436 scl 84974 rsp 52492 rsl 52638 tot 97009
#E tr200 mf9 mn20 scp 86574 scl 86404 rsp 52619 rsl 52638 tot 97009
#G tr200 mf9 mn20 scp 78609 scl 77690 rsp 52870 rsl 52638 tot 97009
LR=0.03
if len(sys.argv)>1:
    COL1=sys.argv[1]
else:
    COL1='B'
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

Xv=pandas.read_csv("train12t%s.csv" % (COL1,))
ridv=Xv.pop('id').apply(str)
lsv=Xv.pop('ls')
lastv=Xv.pop('last')

fo=open('predt'+COL1+'.csv','w')
imp = Imputer(strategy='most_frequent')
for mf in (9,):
    for mn in (20,):
        ttr = 0
        for tr in (200,):
            scp = 0
            scl = 0
            rsp = 0
            rsl = 0
            tot = 0
            xtrain = X.values
            xtrain = imp.fit_transform(xtrain)
            xtest = Xv.values
            xtest = imp.transform(xtest)
            ytrain = y.values
#            rtest = rest.values[test]
#            lstest = ls.values[test]
#            lasttest = last.values[test]
#            anstest = ans.values[test]
            idtest = ridv.values.astype(float)
            m=rgbm.gbm_fit(xtrain,ytrain,nTrain=xtrain.shape[0],var_names=list(X.columns),bag_fraction=1,n_trees=tr,verbose=False,keep_data=False,n_minobsinnode=mn,distribution='multinomial',interaction_depth=mf,shrinkage=LR) #, w=wtrain[rows]*2.0)
            ppp=rgbm.predict_gbm(m,xtest,n_trees=tr,type="response")
            pp = np.array(ppp)
            levels = np.array(ppp.names[1]).astype(int)
            #print pp.shape
            pred=np.argmax(pp,axis=1)
            for i in range(xtest.shape[0]):
                #print '%s %07d %07d %d %s %s' % (idtest[i],anstest[i],lasttest[i],int(levels[pred[i]]),int(levels[pred[i]])==int(a) and rtest[i]==1,lstest[i]==int(a) and rtest[i]==1)
#                if int(lstest[i])==int(a):
#                    scl += 1
#                    if rtest[i]==1:
#                        rsl += 1
#                #fo.write("%07d,%d\n" % (idtest[i],levels[pred[i]]))
                fo.write("%07d,%s\n" % (idtest[i],','.join([str(j[0]) for j in pp[i].tolist()])))
#                aa = '%07d' % anstest[i]
#                ab = '%07d' % lasttest[i]
#                p1 = '%02d' % int(levels[pred[i]])
#                ab=list(ab)
#                ab[ord(COL1)-65] = p1[0]
#                ab=''.join(ab)
#                #print '%s %s %s %d' % ( idtest[i],aa,ab, int(int(levels[pred[i]])==int(a) and rtest[i]==1))
#                if pp[i][pred[i]] > 1.0/len(LEVELS[COL1])+0.1:
#                    if int(levels[pred[i]])==int(a):
#                        scp += 1
#                        if rtest[i]==1:
#                            rsp += 1
#                else:
#                    if int(lstest[i])==int(a):
#                        scp += 1
#                        if rtest[i]==1:
#                            rsp += 1
#                tot += 1
        print '%s tr%d mf%d mn%d scp %d scl %d rsp %d rsl %d tot %d' % (COL1,tr,mf,mn,scp,scl,rsp,rsl,tot)
        sys.stdout.flush()
