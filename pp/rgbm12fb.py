import pandas
import cPickle
import numpy as np
from collections import defaultdict
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
# G 52855
# -2 0.0 tr200 mf7 mn10 scp 0 scl 0 rsp 52659 rsl 52638 tot 97009
# -3 0.0 tr200 mf7 mn10 scp 0 scl 0 rsp 52676 rsl 52638 tot 97009

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

X=pandas.read_csv("train12fb.csv")
rid=X.pop('id').apply(str)
y=X.pop('y')
ans=X.pop('ans')
last=X.pop('last')
pred=X.pop('pred')

fo=open('pred_fbz.csv','w')
imp = Imputer(strategy='most_frequent')
#for mf in (8,11,):
for mf in (8,):
    #for mn in (1,5,20,):
    for mn in (5,30):
        ttr = 0
        #for tr in (200,400,600):
        for tr in (200,400):
            scp = defaultdict(int)
            scl = defaultdict(int)
            rsp = defaultdict(int)
            rsl = defaultdict(int)
            tot = defaultdict(int)
            tsp = defaultdict(int)
            tsl = defaultdict(int)
            kf = KFold(X.shape[0], 3, shuffle=True, random_state=1234)
            for train,test in kf:
                xtrain = X.values[train]
                xtrain = imp.fit_transform(xtrain)
                xtest = X.values[test]
                xtest = imp.transform(xtest)
                ytrain = y.values[train]
                ytest = y.values[test]
                lasttest = last.values[test]
                anstest = ans.values[test]
                predtest = pred.values[test]
                lasttrain = last.values[train]
                anstrain = ans.values[train]
                predtrain = pred.values[train]
                idtest = rid.values[test].astype(float)
                m=rgbm.gbm_fit(xtrain,ytrain,nTrain=xtrain.shape[0],bag_fraction=1,n_trees=tr,verbose=False,keep_data=False,n_minobsinnode=mn,distribution='bernoulli',interaction_depth=mf,shrinkage=LR) #, w=wtrain[rows]*2.0)
                #print rgbm.pretty_gbm_tree(m,1)
                pp=np.array(rgbm.predict_gbm(m,xtest,n_trees=tr))
                pt=np.array(rgbm.predict_gbm(m,xtrain,n_trees=tr))
                #for th in (0.0,0.2):
                for th in (-2.5,-2,-1.5,-1,-0.7,-0.4,):
                    for i,a in enumerate(ytrain):
                        if pt[i]>th:
                            if predtrain[i]==anstrain[i]:
                                tsp[th] += 1
                        else:
                            if lasttrain[i]==anstrain[i]:
                                tsp[th] += 1
                        if lasttrain[i]==anstrain[i]:
                            tsl[th] += 1
                    for i,a in enumerate(ytest):
                        if predtest[i]!=lasttest[i]:
                            fo.write("%07d,%07d,%f,%d,%d,%d\n" % (idtest[i],predtest[i],pp[i],predtest[i]==anstest[i],lasttest[i]==anstest[i],xtest[i][6]))
                        #x1 = '%07d' % lasttest[i]
                        #x2 = '%07d' % predtest[i]
                        #if int(x1[:6]+x2[6])==anstest[i]:
                        #    rsp += 1
                        #if predtest[i]==anstest[i] or lasttest[i]==anstest[i]:
                        #    rsp += 1

                        if pp[i]>th:
                            if predtest[i]==anstest[i]:
                                rsp[th] += 1
                        else:
                            #fo.write("%07d,%07d,%f,%d\n" % (idtest[i],lasttest[i],pp[i],lasttest[i]==anstest[i]))
                            if lasttest[i]==anstest[i]:
                                rsp[th] += 1
                        if lasttest[i]==anstest[i]:
                            rsl[th] += 1
                        tot[th] += 1
            for th in sorted(tot.keys()):
                print 'tr%d mf%d mn%d th %f scp %d scl %d rsp %d rsl %d tot %d %d %d' % (tr,mf,mn,th,scp[th],scl[th],rsp[th],rsl[th],tot[th],tsp[th],tsl[th])
                sys.stdout.flush()
