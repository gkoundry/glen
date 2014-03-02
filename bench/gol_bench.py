import datasets
import pandas
import sys
import gc
import time
import numpy as np
from sklearn.cross_validation import cross_val_score, KFold, train_test_split
from sklearn.linear_model import SGDRegressor, Ridge, LogisticRegression, SGDClassifier, ElasticNet
from tesla.ensemble import RandomForestClassifier
from wrappers.tree_boost import TreeBoost

ds = datasets.get_datasets(name="traind1s")[0]
X, y = datasets.get_data(ds,standardize=False)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.5, random_state=42)
#kf = KFold(X.shape[0], 2, shuffle=True, random_state=1234)
#score_func="log_loss"

#0.010000 log 0.750000 0.251992
#for e in (0.01,):
#    for l in ('log',):
#        for a in (4,2,1,0.75,0.5):
#            clf = SGDClassifier(eta0=e,loss=l,alpha=a)
#            clf.fit(X_train, y_train)
#            p=clf.predict_proba(X_test)
#            print '%f %s %f %f' % (e,l,a,log_loss(y_test, p)) #np.column_stack((1-p,p))))

#clf = CGLM(distribution="Bernoulli")
#clf.fit(X_train, y_train)
#clf = TreeBoost(tree_count=5,min_node_size=ms,mtry=mt,distribution="RandomForest",max_depth=99999)
#p=clf.predict(X_test)
#print log_loss(y_test, np.column_stack((1-p,p)))
#
#sp 0.295693095075 t 3420.74344611
def MAD(act, pred):
    sc = 0
    for i,p in enumerate(pred):
        sc += abs(act[i] - (p > 0.5))
    return sc*1.0/pred.shape[0]

#pred = X_test[:,4]
#print pred
#print MAD(y_test,pred)
##for mt in (2,6,12,18):
#for mt in (14,):
#    #for ms in (2,4,8,16,24,32):
#    for ms in (8,):
#        clf = RandomForestClassifier(n_estimators=500,max_features=mt,min_samples_leaf=ms,n_jobs=-1)
#        clf.fit(X_train, y_train)
#        p1=clf.predict(X_test)
#        print str(mt)+' '+str(ms)+' '+str(MAD(y_test, p1))

for d in range(1,6):
    X=pandas.read_csv('/home/glen/datasets/testdata/traind'+str(d)+'s.dat')
    y=X.pop('y')
    clf = RandomForestClassifier(n_estimators=500,max_features=14,min_samples_leaf=8,n_jobs=-1)
    clf.fit(X, y)
    X=None
    gc.collect()
    X=np.loadtxt('/home/glen/datasets/testdata/testd'+str(d)+'.dat',skiprows=1,delimiter=',')
    y=X[:,0]
    X=np.delete(X,1,1)
    gc.collect()
    pred=clf.predict(X)
    r=X['r']
    c=X['c']
    for i,p in enumerate(pred):
        if r[i]==0 and c[i]==0:
            sys.stdout.write(str(y[i]))
        sys.stdout.write(','+str(int(p>0.5)))
        if r[i]==19 and c[i]==19:
            sys.stdout.write('\n')

