import pandas
import numpy as np
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.cross_validation import train_test_split

# bench = 0.560329453968
# mc/ml mf40 ml5 t200 = 0.544308146926
col = None

def accuracy_score(act,pred):
    c=0
    t=0
    for i in range(act.shape[0]):
        p = pred[i]
        a = act[i]
        if col:
            if p==a:
                c+=1
        else:
            if all(p==a):
                c+=1
        t+=1
    return c*1.0/t

X=pandas.read_csv('trainf.csv')
y=pandas.DataFrame({'A':X.pop('A'),'B':X.pop('B'),'C':X.pop('C'),'D':X.pop('D'),'E':X.pop('E'),'F':X.pop('F'),'G':X.pop('G')})
xtrain,xtest,ytrain,ytest = train_test_split(X,y,test_size=0.6,random_state=42)

for mf in (40,60):
    for mn in (3,5,8):
        m=RandomForestClassifier(n_estimators=200,max_features=mf,min_samples_leaf=mn,n_jobs=3)
        if col:
            m.fit(xtrain,ytrain[:,col])
            p=m.predict(xtest)
            print str(mf)+' '+str(mn)+' '+str(accuracy_score(ytest[:,col],p[:,col]))
        else:
            m.fit(xtrain,ytrain)
            p=m.predict(xtest)
            print str(mf)+' '+str(mn)+' '+str(accuracy_score(ytest,p))
