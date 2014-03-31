import pandas
import cPickle
import sys
from math import log
import numpy as np
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor, AdaBoostClassifier, GradientBoostingClassifier
from sklearn.cross_validation import train_test_split,KFold,cross_val_score
from sklearn.metrics import make_scorer, mean_absolute_error
from sklearn.linear_model import LogisticRegression
from TreeBoost import TreeBoost
#b
#t125 mf4 mn1 0.011762 last 699623 pred 700117 tot 761218 ll 0.249331 0.241351 ym 0.275139
#t150 mf4 mn1 0.008811 last 699623 pred 700127 tot 761218 ll 0.249210 0.240061 ym 0.275139
#t175 mf4 mn1 0.011839 last 699623 pred 700123 tot 761218 ll 0.249187 0.238983 ym 0.275139
#t200 mf4 mn1 0.011778 last 699623 pred 700130 tot 761218 ll 0.249189 0.237948 ym 0.275139
#t300 mf4 mn1 0.009808 last 699623 pred 700063 tot 761218 ll 0.249424 0.234428 ym 0.275139
#a
#t400 mf3 mn1 0.010816 last 699623 pred 700086 tot 761218 ll 0.314307 0.309529 ym 0.275139
#t250 mf4 mn1 0.012872 last 699623 pred 700162 tot 761218 ll 0.312688 0.306284 ym 0.27513
#t350 mf4 mn1 0.013684 last 699623 pred 700197 tot 761218 ll 0.310938 0.302757 ym 0.275139
#t200 mf5 mn1 0.013268 last 699623 pred 700178 tot 761218 ll 0.310191 0.300842 ym 0.275139

MAD = make_scorer(mean_absolute_error, greater_is_better=False)
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

LR=0.05
for trees in (175,):
    for mf in (4,):
    #for mf in (1,2,4,8,16):
        #for mn in (1,5,15,40,):
        for mn in (30,):
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
            ri = None
            for yl in ('A','B','C','D','E','F','G'):
                pred[yl] = {}
                X=pandas.read_csv('train5'+yl+'.csv')
                y=X.pop('y')
                id=X.pop('id')
                cols=X.columns
                test=[[],[],[]]
                train=[[],[],[]]
                if ri is None:
                    ri=pandas.DataFrame({'cols':cols})
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
                #xtrain,xtest,ytrain,ytest = train_test_split(X,y,test_size=0.6,random_state=42)
                #m=RandomForestClassifier(n_estimators=trees,max_features=mf,min_samples_leaf=mn,n_jobs=3,random_state=1234)
                #m=LogisticRegression(C=mf,)
                ll=0
                #for train,test in kf:
                for train,test in cvs:
                    m=TreeBoost()
                    xtrain=X.values[train]
                    xtest=X.values[test]
                    ytrain=y.values[train]
                    ytest=y.values[test]
                    idtest=id.values[test]
                    #m.fit(xtrain,y.values[train])
                    #m.fit(np.ascontiguousarray(xtrain).astype(float),ytrain.astype(float),tree_count=trees,min_node_size=mn,seed=1234,distribution="AdaBoost",max_depth=mf,step_size=LR)
                    m.fit(np.ascontiguousarray(xtrain).astype(float),ytrain.astype(float),tree_count=trees,min_node_size=mn,seed=1234,distribution="Bernoulli",max_depth=mf,step_size=LR)
                    #m.fit(np.ascontiguousarray(xtrain).astype(float),ytrain.astype(float),tree_count=trees,min_node_size=mn,mtry=mf,seed=1234,distribution="RandomForest",max_depth=999)
                    #for t in m.estimators_:
                    #    print 'root '+str(t.tree_.node_count)
                    #    dump(t,0,0)
                    #sys.exit(0)
                    p=m.predict(np.ascontiguousarray(xtest).astype(float))
                    pt=m.predict(np.ascontiguousarray(xtrain).astype(float))
                    #ri[yl+str(ll)]=m.get_relative_influence()
                    ri[yl+str(ll)]=m.get_importance(True)
                    sys.exit(0)
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
                    np.savetxt('testgbm'+yl+'tr'+str(trees)+'mn'+str(mf)+'.out',np.column_stack((ytest,p)),fmt='%f')
                    ll+=1
                    sc1=accuracy_score(ytest,p)
                    sc2=accuracy_score(ytest,np.ones(ytest.shape[0]))
                    ll1+=log_loss(ytest,p)
                    ll1t+=log_loss(ytrain,pt)
                    ll2+=log_loss(ytest,np.repeat(np.mean(ytrain),ytest.shape[0]))
                    tot += sc1-sc2
            print 't%d mf%d mn%d %f LR %f last %d pred %d tot %d ll %f %f ym %f' % (trees,mf,mn,LR,tot,sc1t,sc2t,tt,ll1/ll/7,ll1t/ll/7,ll2/ll/7)
            ri.to_csv('ri.csv')
            #np.savetxt('testp.out',all_pred,fmt='%f')
            #cPickle.dump(pred,open('pred.pkl','wb'))
            #np.savetxt('testy.ouy',all_y,fmt='%f')
