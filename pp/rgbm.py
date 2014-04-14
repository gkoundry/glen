import pandas
import cPickle
import numpy as np
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor, AdaBoostClassifier, GradientBoostingClassifier
from sklearn.preprocessing import Imputer
from math import log
import sys
import rpy2.robjects as robjects
import rpy2.robjects.numpy2ri
rpy2.robjects.numpy2ri.activate()
from rpy2.robjects.numpy2ri import numpy2ri
robjects.conversion.py2ri = numpy2ri
from rpy2.robjects.packages import importr
rgbm = importr("gbm")


iter = 4
#COLS = ['G']
COLS = ['A','B','C','G']
#COLS = ['A','B','C','D','E','F','G']
LEVELS={
    'A': ('0','1','2'),
    'B': ('0','1'),
    'C': ('1','2','3','4'),
    'D': ('1','2','3'),
    'E': ('0','1'),
    'F': ('0','1','2','3'),
    'G': ('1','2','3','4'),
}

def log_loss(a,p):
    sc = 0
    for i in range(a.shape[0]):
        ps=0
        for j in LEVELS[COL]:
            ps += p[j][i]
        for j in LEVELS[COL]:
            p[j][i] /= ps
        pred = p[str(a[i])][i]
        if pred<0.001:
            pred=0.001
        if pred>0.999:
            pred=0.999
        sc -= log(pred)
        #sc -= a[i]*log(pred)+(1-a[i])*log(1-pred)
    return sc/a.shape[0]

def dump(t,n,l):
    if n>=0 and t.tree_.feature[n]>=0:
        print ' '*l+' f'+str(t.tree_.feature[n])+' <= '+str(t.tree_.threshold[n])+' '+str(t.tree_.n_node_samples[t.tree_.children_left[n]])+' '+str(t.tree_.value[t.tree_.children_left[n]])
        dump(t,t.tree_.children_left[n],l+1)
        print ' '*l+' f'+str(t.tree_.feature[n])+' > '+str(t.tree_.threshold[n])+' '+str(t.tree_.n_node_samples[t.tree_.children_right[n]])+' '+str(t.tree_.value[t.tree_.children_right[n]])
        dump(t,t.tree_.children_right[n],l+1)

for COL in COLS:
    print COL
    X=pandas.read_csv("train6%s%d.csv" % (COL,iter))
    rid=X.pop('id').apply(str)
    wt=X.pop('wt')
    rest=X.pop('rest')
    cvp = ([r'[12467]$',r'[35890]$'],[r'[35890]$',r'[12467]$'])
    ls=X.pop('ls')
    csls=X.pop('csls')
    y=X.pop('y')

    imp = Imputer(strategy='most_frequent')
    LR=0.02
    SS=80000
    #for mf in (2,5,10):
    for mf in (4,):
        #for mn in (2,10,30,100):
        for mn in (1,):
            m={}
            ttr = 0
            save = {}
            for tr in (200,):
                ttr += tr
                pp = None
                cvpp = []
                cvppt = []
                lstest = []
                idtest = []
                rtest = []
                ya = []
                yat = []
                cvi = 0
                scp = 0
                scl = 0
                rsp = 0
                rsl = 0
                tot = 0
                for cv in cvp:
                    train=rid.str.contains(cv[0])
                    test=rid.str.contains(cv[1])
                    xtrain = X.values[train]
                    xtrain = imp.fit_transform(xtrain)
                    xtest = X.values[test]
                    xtest = imp.transform(xtest)
                    ytrain = y.values[train]
                    ytest = y.values[test]
                    rtest.extend(rest.values[test].tolist())
                    wtrain = wt.values[train]
                    idtest.extend(rid.values[test].tolist())
                    ya.extend(ytest.tolist())
                    yat.extend(ytrain.tolist())

                    rows = np.arange(ytrain.shape[0])
                    np.random.seed(1234)
                    np.random.shuffle(rows)
                    rows = sorted(rows[:SS,])
                    xtrainm = robjects.r['matrix'](xtrain[rows],ncol=xtrain.shape[1],dimnames=[[],['X%d' % (i+1) for i in range(xtrain.shape[1])]])
                    m=rgbm.gbm_fit(xtrainm,ytrain[rows],n_trees=tr,verbose=False,keep_data=True,n_minobsinnode=mn,distribution="multinomial",interaction_depth=mf,shrinkage=LR) #, w=wtrain[rows]*2.0)
                    if pp==None:
                        pp = rgbm.predict_gbm(m,xtest,n_trees=tr,type="response")
                    else:
                        pp = np.concatenate((pp,rgbm.predict_gbm(m,xtest,n_trees=tr,type="response")))
#                    if cvi in m:
#                        #m[cvi] = rgbm.gbm_more(m[cvi],n_new_trees=tr,data=xtrainm)
#                        m[cvi]=rgbm.gbm_fit(xtrainm,ytrain[rows],n_trees=tr,verbose=False,keep_data=True,n_minobsinnode=mn,distribution="multinomial",interaction_depth=mf,shrinkage=LR) #, w=wtrain[rows]*2.0)
#                        pp = np.concatenate((pp,rgbm.predict_gbm(m[cvi],xtest,n_trees=ttr,type="response")))
#                    else:
#                        m[cvi]=rgbm.gbm_fit(xtrainm,ytrain[rows],n_trees=tr,verbose=False,keep_data=True,n_minobsinnode=mn,distribution="multinomial",interaction_depth=mf,shrinkage=LR) #, w=wtrain[rows]*2.0)
#                        #df = robjects.r['data.frame'](xtrain[rows],y=ytrain[rows])
#                        #formula = robjects.r['as.formula']('as.factor(y) ~ '+' + '.join(['X%d' % (i+1) for i in range(xtrain.shape[1])]))
#                        #m[cvi]=rgbm.gbm(formula,data=df,n_trees=tr,verbose=False,keep_data=True,n_minobsinnode=mn,distribution="multinomial",interaction_depth=mf,shrinkage=LR) #, w=wtrain[rows]*2.0)
#                        #print rgbm.pretty_gbm_tree(m[cvi])
#                        #m[cvi]=rgbm.gbm_fit(xtrain[rows],ytrain[rows],n_trees=tr,verbose=False,keep_data=True,n_minobsinnode=mn,distribution="multinomial",interaction_depth=mf,shrinkage=LR) #, w=wtrain[rows]*2.0)
#                        #dfv = robjects.r['data.frame'](xtest)
#                        if pp==None:
#                            pp = rgbm.predict_gbm(m[cvi],xtest,n_trees=ttr,type="response")
#                        else:
#                            pp = np.concatenate((pp,rgbm.predict_gbm(m[cvi],xtest,n_trees=ttr,type="response")))
#                        #m[cvi][val]=rgbm.gbm_fit(xtrain[rows],ytrain[rows],n_trees=tr,verbose=False,keep_data=True,n_minobsinnode=mn,distribution="bernoulli",interaction_depth=mf,shrinkage=LR) #, w=wtrain[rows]*2.0)
                    #print zip(X.columns,[round(i,5) for i in m[val].get_importance(False,np.ascontiguousarray(xtest).astype(float),ytest_.astype(float))])
                    #cvpp.extend(rgbm.predict_gbm(m[cvi],xtest,n_trees=ttr,type="response"))
                    #cvppt.extend(rgbm.predict_gbm(m[cvi],xtrain,n_trees=ttr,type="response"))
                    #pt = m.predict(np.ascontiguousarray(xtrain).astype(float))

                    #np.savetxt('test.out',np.column_stack((pp['0'],pp['1'],pp['2'],ls.values[test].astype(float))),fmt='%f')
                    #print pp
                    lstest.extend( ls.values[test].tolist())
                    cvi+=1
                pred=np.argmax(pp,axis=1)+int(LEVELS[COL][0])
                save.update(dict(zip(idtest,pred)))
                for i,a in enumerate(ya):
                    p=pred[i]
                    if int(p)==a:
                        scp += 1
                        if rtest[i]==1:
                            rsp += 1
                    if lstest[i]==a:
                        scl += 1
                        if rtest[i]==1:
                            rsl += 1
                    tot += 1
                llp = 0 #log_loss(np.array(ya),cvpp)
                llpt = 0 #log_loss(np.array(yat),cvppt)
                print 'tr %d ss %d mf %d mn %d p %d l %d t %d llp %f llv %f rsp %d rsl %d' % (ttr,SS,mf,mn,scp,scl,tot,llp,llpt,rsp,rsl)
                cPickle.dump(save,open('pred'+COL+str(iter)+'.out','wb'))
