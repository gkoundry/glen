import pandas
import math
import cPickle
import numpy as np
from sklearn.preprocessing import Imputer
from sklearn.cross_validation import train_test_split,KFold,cross_val_score
from sklearn.linear_model import SGDClassifier,LogisticRegression
from math import log
import sys
import rpy2.robjects as robjects
import rpy2.robjects.numpy2ri
rpy2.robjects.numpy2ri.activate()
from rpy2.robjects.numpy2ri import numpy2ri
robjects.conversion.py2ri = numpy2ri
from rpy2.robjects.packages import importr
rgbm = importr("gbm")

def AMS(s, b):
    """ Approximate Median Significance defined as:
        AMS = sqrt(
                2 { (s + b + b_r) log[1 + (s/(b+b_r))] - s}
              )
    where b_r = 10, b = background, s = signal, log is natural logarithm """

    br = 10.0
    radicand = 2 *( (s+b+br) * math.log (1.0 + s/(b+br)) -s)
    if radicand < 0:
        print 'radicand is negative. Exiting'
        exit()
    else:
        return math.sqrt(radicand)

LR=0.1

X=pandas.read_csv("training.csv",na_values='-999.0')
w=X.pop('Weight')
y=X.pop('Label')
y=(y=='s').astype(int)
eid=X['EventId']

Xt=pandas.read_csv("test.csv")
eidt=Xt['EventId']

#imp = Imputer(strategy='most_frequent')
mf=7
mn=200
tr=500
fo=open('predrgbm_%d_%f_%d_p.csv' % (tr,LR,mn),'w')
xtrain = X.values
#                xtrain = imp.fit_transform(xtrain)
xtest = Xt.values
#                xtest = imp.transform(xtest)
ytrain = y.values
wtrain = w.values
eidtrain = eid.values
eidtest = eidt.values
#m=LogisticRegression()
#m=SGDClassifier(alpha=0.000001,loss='log')
#m.fit(xtrain,ytrain)
#pp=m.predict_proba(xtest)[:,1]
m=rgbm.gbm_fit(xtrain,ytrain,nTrain=xtrain.shape[0],var_names=list(X.columns),bag_fraction=1,n_trees=tr,verbose=False,keep_data=False,n_minobsinnode=mn,distribution='bernoulli',interaction_depth=mf,shrinkage=LR) #, w=wtrain[rows]*2.0)
ppp=rgbm.predict_gbm(m,xtest,n_trees=tr,type="response")
pp = np.array(ppp)
#print pp.shape
for i,a in enumerate(eidtest):
    fo.write('%s,%f\n' % (eidtest[i],pp[i]))
