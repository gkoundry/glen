import datasets
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
    cor = ace(Xc, yc, datasets.get_column_index(ds))
    base = run_rf(ds)
    for i,c in enumerate(datasets.get_columns(ds)):
        print '%-30s,%f,%f' % (c,base-run_rf(ds,[i]),cor[i])
