import datasets
import time
from wrappers.tree_boost import TreeBoost
from tesla.ensemble import RandomForestClassifier, RandomForestRegressor
from tesla.ensemble import ExtraTreesClassifier, ExtraTreesRegressor
from sklearn.ensemble import RandomForestClassifier as RandomForestClassifierSk, RandomForestRegressor as RandomForestRegressorSk
from sklearn.cross_validation import cross_val_score, KFold
from sklearn.metrics import make_scorer, mean_absolute_error

MAD = make_scorer(mean_absolute_error, greater_is_better=False)

for ds in datasets.get_datasets():
    X, y = datasets.get_data(ds)
    kf = KFold(X.shape[0], 5, shuffle=True, random_state=1234)
    if ds['rtype'] == 'Binary':
        clf1 = TreeBoost(tree_count=200, mtry='auto', min_node_size=5,distribution="Bernoulli")
        clf2 = ExtraTreesClassifier(n_estimators=200,min_samples_leaf=5,max_features='sqrt')
        clf3 = RandomForestClassifier(n_estimators=200,min_samples_leaf=5,max_features='sqrt')
        clf4 = RandomForestClassifierSk(n_estimators=200,min_samples_leaf=5,max_features='sqrt')
        score_func = 'log_loss'
    else:
        clf1 = TreeBoost(tree_count=200, mtry='auto', min_node_size=5,distribution="Gaussian")
        clf2 = ExtraTreesRegressor(n_estimators=200,min_samples_leaf=5,max_features='sqrt')
        clf3 = RandomForestRegressor(n_estimators=200,min_samples_leaf=5,max_features='sqrt')
        clf4 = RandomForestRegressorSk(n_estimators=200,min_samples_leaf=5,max_features='sqrt')
        score_func = MAD
    for clf in (clf1, clf2, clf3, clf4):
        st = time.time()
        print '%-20s %20s sc %9.4f tm %5.2f' % \
              (ds['name'], clf.__class__.__name__,
               cross_val_score(clf, X, y, cv=kf, scoring=score_func, n_jobs=3).mean(), time.time()-st)
