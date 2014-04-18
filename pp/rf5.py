from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor, AdaBoostClassifier, GradientBoostingClassifier
from sklearn.cross_validation import train_test_split,KFold,cross_val_score
import pandas
import sys
X=pandas.read_csv('traint1.csv')
ans = X.pop('ans')
l_ans = X.pop('l_ans')
y = X.pop('y')

for tr in (200,):
    for mf in (7,15,):
        for mn in (3,25):
            m=RandomForestClassifier(n_estimators=tr,max_features=mf,min_samples_leaf=mn,n_jobs=1,random_state=1234)
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
                m.fit(xtrain,ytrain)
                p=m.predict_proba(xtest)[:,1]
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
