import pandas
from math import log
import numpy as np
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor, AdaBoostClassifier, GradientBoostingClassifier
from sklearn.cross_validation import train_test_split,KFold,cross_val_score
from sklearn.metrics import make_scorer, mean_absolute_error
from sklearn.linear_model import LogisticRegression

MAD = make_scorer(mean_absolute_error, greater_is_better=False)
# bench=0.560329453968
# 10 30 t500 0.541129780435
# 40 30 t200 0.559272239975
# 40 30 t500 0.559272239975
# 60 300 0.559942273992
#4 64 0.002068 last 44169 pred 44171 tot 51445 ll 0.375124

def log_loss(act,pred):
    c=0
    t=0
    for i in range(act.shape[0]):
        p = pred[i]
        a = act[i]
        if p>0.999:
            p=0.999
        if p<0.001:
            p=0.001
        c+=a*log(p)+(1-a)*log(1-p)
        t+=1
    return -c*1.0/t

def accuracy_score(act,pred):
    c=0
    t=0
    for i in range(act.shape[0]):
        p = pred[i]
        a = act[i]
        if p>0.5:
            p=1
        else:
            p=0
        if p==a:
            c+=1
        t+=1
    return c*1.0/t

def dump(t,n,l):
    if n>=0 and t.tree_.feature[n]>=0:
        print ' '*l+' f'+str(t.tree_.feature[n])+' <= '+str(t.tree_.threshold[n])+' '+str(t.tree_.n_node_samples[t.tree_.children_left[n]])+' '+str(t.tree_.value[t.tree_.children_left[n]])
        dump(t,t.tree_.children_left[n],l+1)
        print ' '*l+' f'+str(t.tree_.feature[n])+' > '+str(t.tree_.threshold[n])+' '+str(t.tree_.n_node_samples[t.tree_.children_right[n]])+' '+str(t.tree_.value[t.tree_.children_right[n]])
        dump(t,t.tree_.children_right[n],l+1)

#for mf in (3,4,6,):
for mf in (1,2,4,8,):
    for mn in (4,8,16,32,64,128):
    #for mn in (40,52,64,80,100,):
        tot=0
        #all_pred=None
        #all_y=None
        #idp=None
        sc1t=0
        sc2t=0
        tt=0
        ll1=0
        ll2=0
        X=pandas.read_csv('train3.csv')
        y=X.pop('y')
        id=X.pop('id')
        kf = KFold(X.shape[0], 10, shuffle=True, random_state=1234)
        m=RandomForestClassifier(n_estimators=100,max_features=mf,min_samples_leaf=mn,n_jobs=3,random_state=1234)
        i=0
        for train,test in kf:
            xtrain=X.values[train]
            xtest=X.values[test]
            ytest=y.values[test]
            idtest=id.values[test]
            m.fit(xtrain,y.values[train])
            p=m.predict_proba(xtest)[:,1]
            for i in range(xtest.shape[0]):
                if ytest[i]==1:
                    sc1t+=1
                if p[i]>0.5:
                    if ytest[i]==1:
                        sc2t+=1
                else:
                    if ytest[i]==0:
                        sc2t+=1
                tt += 1
            i+=1
            sc1=accuracy_score(y.values[test],p)
            sc2=accuracy_score(y.values[test],np.ones(y.values[test].shape[0]))
            ll1+=log_loss(y.values[test],p)
            ll2+=log_loss(y.values[test],np.ones(y.values[test].shape[0]))
            tot += sc1-sc2
        print '%d %d %f last %d pred %d tot %d ll %f' % (mf,mn,tot,sc1t,sc2t,tt,ll1/10)
    #np.savetxt('testp.out',all_pred,fmt='%f')
    #np.savetxt('testy.ouy',all_y,fmt='%f')
