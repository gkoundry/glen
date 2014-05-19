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

LR=0.01
LEVELS={
    'A': ('0','1','2'),
    'B': ('0','1'),
    'C': ('1','2','3','4'),
    'D': ('1','2','3'),
    'E': ('0','1'),
    'F': ('0','1','2','3'),
    'G': ('1','2','3','4'),
}

X=pandas.read_csv("train12fbp.csv")
rid=X.pop('id').apply(str)
y=X.pop('y')
mask1=y==-1
mask2=y==0
mask3=y==1
mask4=y==6
ans=X.pop('ans')
last=X.pop('last')
pred=X.pop('pred')
pred2=X.pop('pred2')
#pred[pred==last]=pred2[pred==last]
#diff=X.pop('diff')
#x1=X.pop('prp')
#x1=X.pop('prl')
#x1=X.pop('prrt')

fo=open('pred_fbg.csv','w')
imp = Imputer(strategy='most_frequent')
#for mf in (8,11,):

   #-1
#-3  0
#-2  1  1  3
#-1     2  4
       #3  5
#-4 0 0 2
#-3 0 0 1
#for y1 in (-3,):
#    for y2 in (0,):
#        for y3 in (0,):
#            for y4 in (2,):
for y1 in (0,):
    for y2 in (10,):
        for y3 in (10,):
            for y4 in (20,):
                y[mask1]=y1
                y[mask2]=y2
                y[mask3]=y3
                y[mask4]=y4
                for mf in (7,):
                    #for mn in (1,5,20,):
                    for mn in (10,):
                        ttr = 0
                        #for tr in (200,400,600):
                        for tr in (200,):
                            scp = defaultdict(int)
                            scl = defaultdict(int)
                            rsp = defaultdict(int)
                            rsl = defaultdict(int)
                            df1 = defaultdict(int)
                            df2 = defaultdict(int)
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
                                pred2test = pred2.values[test]
                                lasttrain = last.values[train]
                                anstrain = ans.values[train]
                                predtrain = pred.values[train]
                                pred2train = pred2.values[train]
                                idtest = rid.values[test].astype(float)
                                #xtrain1=xtrain[np.logical_or(lasttrain!=predtrain,lasttrain!=pred2train)]
                                #ytrain1=ytrain[np.logical_or(lasttrain!=predtrain,lasttrain!=pred2train)]
                                xtrain1=xtrain[lasttrain!=predtrain]
                                ytrain1=ytrain[lasttrain!=predtrain]
                                m=rgbm.gbm_fit(xtrain1,ytrain1,nTrain=xtrain1.shape[0],bag_fraction=1,n_trees=tr,verbose=False,keep_data=False,n_minobsinnode=mn,distribution='gaussian',interaction_depth=mf,shrinkage=LR) #, w=wtrain[rows]*2.0)
                                #m=rgbm.gbm_fit(xtrain[lasttrain!=predtrain],ytrain[lasttrain!=predtrain],nTrain=xtrain[lasttrain!=predtrain].shape[0],bag_fraction=1,n_trees=tr,verbose=False,keep_data=False,n_minobsinnode=mn,distribution='gaussian',interaction_depth=mf,shrinkage=LR) #, w=wtrain[rows]*2.0)
                                #m=rgbm.gbm_fit(xtrain,ytrain,nTrain=xtrain.shape[0],bag_fraction=1,n_trees=tr,verbose=False,keep_data=False,n_minobsinnode=mn,distribution='gaussian',interaction_depth=mf,shrinkage=LR) #, w=wtrain[rows]*2.0)
                                #print rgbm.pretty_gbm_tree(m,1)
                                pp=np.array(rgbm.predict_gbm(m,xtest,n_trees=tr))
                                pt=np.array(rgbm.predict_gbm(m,xtrain,n_trees=tr))
                                if len(tot.keys())==0:
                                    pp1=pp.min()
                                    pp2=pp.max()
                                for th in np.linspace(pp1,pp2,20):
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

                                        if predtest[i]!=lasttest[i]:
                                            if predtest[i]==anstest[i]:
                                                df1[th] += 1
                                            else:
                                                df2[th] += 1
                                        if pp[i]>th:
                                            if predtest[i]!=lasttest[i]:
                                                scp[th] += 1
                                            if predtest[i]==anstest[i]:
                                                rsp[th] += 1
                                                if predtest[i]!=lasttest[i]:
                                                    scl[th] += 1
                                        else:
                                            #fo.write("%07d,%07d,%f,%d\n" % (idtest[i],lasttest[i],pp[i],lasttest[i]==anstest[i]))
                                            if lasttest[i]==anstest[i]:
                                                rsp[th] += 1
                                        if lasttest[i]==anstest[i]:
                                            rsl[th] += 1
                                        tot[th] += 1
                            for th in sorted(tot.keys()):
                                print '%d %d %d %d tr%d mf%d mn%d th %f df1 %d df2 %d scp %d scl %d rsp %d rsl %d tot %d %d %d' % (y1,y2,y3,y4,tr,mf,mn,th,df1[th],df2[th],scp[th],scl[th],rsp[th],rsl[th],tot[th],tsp[th],tsl[th])
                                sys.stdout.flush()
