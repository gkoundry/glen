import numpy as np
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
import datasets
from sklearn.cross_validation import cross_val_score, KFold
from sklearn.metrics import make_scorer, mean_absolute_error
from wrappers.correlation import ace,rcorrs,rcorrp, bcdcor
from collections import defaultdict

MAD = make_scorer(mean_absolute_error, greater_is_better=False)

sc=defaultdict(lambda:defaultdict(lambda:defaultdict(int)))
for ds in datasets.get_datasets():
    Xc, yc = datasets.get_data(ds, convert='numbers', standardize=False)
    kf = KFold(Xc.shape[0], 5, shuffle=True)
    for vi in (bcdcor, rcorrp, rcorrs, ace):
        cor = vi(Xc, yc, datasets.get_column_index(ds))
        #print zip(ds['category']+ds['numeric'],cor)
        for drop in range(10):
            vi_name = vi.__name__
            X, y = datasets.get_data(ds, drop=np.argsort(cor)[:drop])
            if ds['rtype'] == 'Binary':
                metric = 'log_loss'
                clf = RandomForestClassifier(n_estimators=200,min_samples_leaf=5,n_jobs=1)
            else:
                metric = MAD
                clf = RandomForestRegressor(n_estimators=200,min_samples_leaf=5,n_jobs=1)
            sc[ds['name']][vi_name][drop] = cross_val_score(clf, X, y, cv=kf, n_jobs=3, scoring=metric).mean()
            print ds['name']+' '+vi_name+" "+str(drop)+' '+str(sc[ds['name']][vi_name][drop])
