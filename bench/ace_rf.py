import datasets
import numpy as np
from sklearn.cross_validation import cross_val_score, KFold
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from wrappers.correlation import ace
from sklearn.metrics import make_scorer, mean_absolute_error

MAD = make_scorer(mean_absolute_error, greater_is_better=False)

def run_rf(ds, drop=[]):
    X, y = datasets.get_data(ds, drop=drop)
    kf = KFold(X.shape[0], 5, shuffle=True, random_state=1234)
    if ds['rtype'] == 'Binary':
        metric = 'log_loss'
        clf = RandomForestClassifier(n_estimators=200,min_samples_leaf=5,n_jobs=1)
    else:
        metric = MAD
        clf = RandomForestRegressor(n_estimators=200,min_samples_leaf=5,n_jobs=1)
    return cross_val_score(clf, X, y, cv=kf, n_jobs=3, scoring=metric).mean()

for ds in datasets.get_datasets():
    Xc, yc = datasets.get_data(ds, convert='numbers', standardize=False)
    #cor = ace(Xc, yc, datasets.get_column_index(ds),ds['rtype'])
    cor = ace(Xc, yc, range(0,Xc.shape[1]),ds['rtype'])
    ncor = ace(Xc, yc, [],ds['rtype'])
    #print '==== '+ds['name']+' ===='
    #print zip(datasets.get_columns(ds),cor)
    for i,c in enumerate(datasets.get_columns(ds)):
        acat = cor[i]-len(np.unique(Xc[:,i]))*1.0/Xc.shape[0]
        if i in datasets.get_column_index(ds):
            htype = 'CAT'
            tcat = acat
        else:
            htype = 'NUM'
            tcat = ncor[i]
        print ds['name']+','+c+','+htype+','+str(ncor[i])+','+str(cor[i])+','+str(acat)+','+str(tcat)
    #print ''
    #base = run_rf(ds)
    #for i,c in enumerate(datasets.get_columns(ds)):
    #    print '%-30s,%f,%f' % (c,base-run_rf(ds,[i]),cor[i])
