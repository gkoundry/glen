import pandas
import cPickle
import sys
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

for trees in (100,150,200):
    for mf in (2,3,4,):
    #for mf in (1,2,4,8,16):
        for mn in (1,):
        #for mn in (1,3,5,9,17,33,65,129,259):
            tot=0
            all_pred=None
            #all_y=None
            idp=None
            sc1t=0
            sc2t=0
            tt=0
            ll1=0
            ll1t=0
            ll2=0
            pred={}
            for yl in ('A','B','C','D','E','F','G'):
                X=pandas.read_csv('train4'+yl+'.csv')
                y=X.pop('y')
                id=X.pop('id')
                pred[yl] = {}
                test=[[],[],[]]
                train=[[],[],[]]
                for i in range(id.shape[0]):
                    if int(str(id[i])[-2:])<33:
                        test[0].append(i)
                        train[1].append(i)
                        train[2].append(i)
                    elif int(str(id[i])[-2:])<66:
                        train[0].append(i)
                        test[1].append(i)
                        train[2].append(i)
                    else:
                        train[0].append(i)
                        train[1].append(i)
                        test[2].append(i)
                cvs = [[train[0],test[0]],[train[1],test[1]],[train[2],test[2]]]
                #prt=X.pop('prrt')
    #            if all_y is None:
    #                all_y=np.copy(y)
    #            else:
    #                print y.shape
    #                print all_y.shape
    #                all_y=np.column_stack([all_y,np.copy(y)])
                #freq=dict(pandas.DataFrame({'y':y}).groupby('y').count()['y'])
                #X['mfpr']=X['mf']
                #X['mfpr'].apply(lambda x:freq[x])
                #X['lspr']=X['last']
                #X['lspr'].apply(lambda x:freq[x])
                #kf = KFold(X.shape[0], 10, shuffle=True, random_state=1234)
                xtrain,xtest,ytrain,ytest = train_test_split(X,y,test_size=0.6,random_state=42)
                #m=RandomForestClassifier(n_estimators=trees,max_features=mf,min_samples_leaf=mn,n_jobs=3,random_state=1234)
                #m=LogisticRegression(C=mf,)
                m=GradientBoostingClassifier(n_estimators=trees,learning_rate=0.03,min_samples_leaf=mn,max_depth=mf)
                ll=0
                #for train,test in kf:
                for train,test in cvs:
                    xtrain=X.values[train]
                    xtest=X.values[test]
                    ytest=y.values[test]
                    idtest=id.values[test]
                    m.fit(xtrain,y.values[train])
                    #for t in m.estimators_:
                    #    print 'root '+str(t.tree_.node_count)
                    #    dump(t,0,0)
                    #sys.exit(0)
                    p=m.predict_proba(xtest)[:,1]
                    pt=m.predict_proba(xtrain)[:,1]
                    #p=np.ones(p.shape[0])
                    for i in range(xtest.shape[0]):
                        if ytest[i]==1:
                            sc1t+=1
                        if p[i]>0.5:
                            pred[yl][idtest[i]]=xtest[i][0]
                            if ytest[i]==1:
                                sc2t+=1
                        else:
                            pred[yl][idtest[i]]=xtest[i][1]
                            if ytest[i]==0:
                                sc2t+=1
                        tt += 1
                    np.savetxt('testg'+str(i)+yl+'.out',np.column_stack((y.values[test],p)),fmt='%f')
                    ll+=1
                    sc1=accuracy_score(y.values[test],p)
                    sc2=accuracy_score(y.values[test],np.ones(y.values[test].shape[0]))
                    ll1+=log_loss(y.values[test],p)
                    ll1t+=log_loss(y.values[train],pt)
                    ll2+=log_loss(y.values[test],np.ones(y.values[test].shape[0]))
                    tot += sc1-sc2
            print 't%d mf%d mn%d %f last %d pred %d tot %d ll %f %f' % (trees,mf,mn,tot,sc1t,sc2t,tt,ll1/ll/7,ll1t/ll/7)
            #np.savetxt('testp.out',all_pred,fmt='%f')
            #cPickle.dump(pred,open('pred.pkl','wb'))
            #np.savetxt('testy.ouy',all_y,fmt='%f')
