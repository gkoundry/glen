from sklearn.cross_validation import train_test_split,KFold,cross_val_score
import numpy as np
import pandas
import sys
import rpy2.robjects as robjects
import rpy2.robjects.numpy2ri
rpy2.robjects.numpy2ri.activate()
from rpy2.robjects.numpy2ri import numpy2ri
robjects.conversion.py2ri = numpy2ri
from rpy2.robjects.packages import importr
rgbm = importr("gbm")
X=pandas.read_csv('traint1.csv')
ans = X.pop('ans')
l_ans = X.pop('l_ans')
y = X.pop('y')

dist = 'bernoulli'
LR =0.02
for tr in (10,100,200,300,400,):
    for mf in (5,8,):
        for mn in (3,25):
            kf = KFold(X.shape[0], 3, shuffle=True, random_state=1234)
            scl = 0
            scp = 0
            ecl = 0
            ecp = 0
            tot = 0
            diff = 0
            for train,test in kf:
                xtrain = X.values[train]
                xtest = X.values[test]
                ytrain = y.values[train]
                ytest = y.values[test]
                atest = ans.values[test]
                ltest = l_ans.values[test]
                m=rgbm.gbm_fit(xtrain,ytrain,nTrain=xtrain.shape[0],bag_fraction=1,n_trees=tr,verbose=False,keep_data=True,n_minobsinnode=mn,distribution=dist,interaction_depth=mf,shrinkage=LR) #, w=wtrain[rows]*2.0)
                p = np.array(rgbm.predict_gbm(m,xtest,n_trees=tr,type="response"))
                for i in range(atest.shape[0]):
                    if atest[i]==ltest[i]:
                        scl += 1
                    sl = '%07d' % ltest[i]
                    sa = '%07d' % atest[i]
                    #print sa +' '+sl+' '+str(p[i])+' '+str(y[i])+' '+sl[4]
                    if sa==sl[0:4]+str(int(p[i]>0.5))+sl[5:]:
                        scp += 1
                    if int(p[i]>0.5)==int(sa[4]):
                        ecp += 1
                    if sl[4]==sa[4]:
                        ecl += 1
                    if int(sl[4])!=int(p[i]>0.5):
                        diff += 1
                    tot += 1
            print 'tr%d mf%d mn%d %d %d %d %d %d diff %d' % (tr,mf,mn,ecp,ecl,scp,scl,tot,diff)
            sys.stdout.flush()
