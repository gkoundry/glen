import pandas
import numpy as np
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.cross_validation import train_test_split

# bench=0.560329453968
# 10 30 t500 0.541129780435
# 40 30 t200 0.559272239975
# 40 30 t500 0.559272239975
# 60 300 0.559942273992

def accuracy_score(act,pred):
    c=0
    t=0
    for i in range(act.shape[0]):
        p = pred[i]
        a = act[i]
        if all(p==a):
            c+=1
        t+=1
    return c*1.0/t

X=pandas.read_csv('trainf2i.csv')
y=pandas.DataFrame({'A':X.pop('A'),'B':X.pop('B'),'C':X.pop('C'),'D':X.pop('D'),'E':X.pop('E'),'F':X.pop('F'),'G':X.pop('G')})
xtrain,xtest,ytrain,ytest = train_test_split(X,y,test_size=0.6,random_state=42)

for mf in (7,):
    for mn in (70,):
        p = []
        for col in range(7):
            m=RandomForestClassifier(n_estimators=200,max_features=mf,min_samples_leaf=mn,n_jobs=3)
            m.fit(xtrain,ytrain[:,col])
            p.append(m.predict(xtest))
        print str(mf)+' '+str(mn)+' '+str(accuracy_score(ytest,np.column_stack(p)))
        for i in range(xtest.shape[0]):
            print str(xtest[i][0])+' '+''.join([str(j) for j in np.column_stack(p)[i].tolist()])
