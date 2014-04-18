from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor, AdaBoostClassifier, GradientBoostingClassifier
import pandas
X=pandas.read_csv('traint1.csv')
ans = X.pop('ans')
l_ans = X.pop('l_ans')
y = X.pop('y')
m=RandomForestClassifier(n_estimators=3,max_features=4,min_samples_leaf=20,n_jobs=3,random_state=1234)
m.fit(X,y)
p=m.predict_proba(X)[:,1]
scl = 0
scp = 0
tot = 0
for i in range(ans.shape[0]):
    if ans[i]==l_ans[i]:
        scl += 1
    sl = '%07d' % l_ans[i]
    #print ('%07d' % ans[i]) +' '+sl[0:4]+str(int(p[i]>0.5))+sl[5:]
    if ('%07d' % ans[i])==sl[0:4]+str(int(p[i]>0.5))+sl[5:]:
        scp += 1
    tot += 1
print '%d %d %d' % (scp,scl,tot)
