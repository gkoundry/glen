from tesla.ensemble import GradientBoostingClassifier
from sklearn.cross_validation import cross_val_score, KFold
from math import sqrt
import datasets
import sys

score_func='roc_auc'
#for ds in datasets.get_datasets(name='kickcars_small'):
for ds in datasets.get_datasets(name='kickcars_train_full'):
    X, y = datasets.get_data(ds,standardize=False)
    kf = KFold(X.shape[0], 2, shuffle=True, random_state=1234)
    #for lr in (0.1,0.05,0.01):
    #for lr in (0.05,):
        #for md in (2,3,4):
    lr=0.05
    for md in (2,3,4):
        for ms in (1,):
            t=100
            td=100
            bestsc = 0
            bestt = 40
            incr=0
            while True:
                clf = GradientBoostingClassifier(min_samples_leaf=ms,learning_rate=0.05,max_depth=md,n_estimators=t)
                sc = cross_val_score(clf, X, y, cv=kf, scoring=score_func, n_jobs=-1).mean()
                print '%f %d %d %d %f' % (lr,md,ms,t,sc)
                if sc > bestsc:
                    bestsc=sc
                    bestt=t
                    incr=0
                    td *= 2
                else:
                    t-=td
                    td = int(sqrt(t)*2)
                    incr += 1
                if incr>4:
                    break
                t+=td
                sys.stdout.flush()
            print '* %f %d %d %d %f' % (lr,md,ms,bestt,bestsc)
            print ''
            sys.stdout.flush()
