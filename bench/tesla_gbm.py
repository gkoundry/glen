from tesla.ensemble import GradientBoostingClassifier
from sklearn.cross_validation import cross_val_score, KFold
import datasets

score_func='roc_auc'
#for ds in datasets.get_datasets(name='kickcars_small'):
for ds in datasets.get_datasets(name='kickcars_train_full'):
    X, y = datasets.get_data(ds,standardize=False)
    kf = KFold(X.shape[0], 2, shuffle=True, random_state=1234)
    for lr in (0.1,0.05,0.01):
        for md in (1,3,5):
            t=40
            bestsc = 0
            bestt = 40
            incr=0
            while True:
                clf = GradientBoostingClassifier(learning_rate=lr,max_depth=md,n_estimators=t)
                sc = cross_val_score(clf, X, y, cv=kf, scoring=score_func, n_jobs=-1).mean()
                if sc > bestsc:
                    bestsc=sc
                    bestt=t
                    incr=0
                else:
                    incr += 1
                if incr>4:
                    break
                print '%f %d %d %f' % (lr,md,t,sc)
                t+=20
            print '* %f %d %d %f' % (lr,md,bestt,bestsc)
            print ''
