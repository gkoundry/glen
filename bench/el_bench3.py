import datasets
from wrappers.elastic_net_c import ElasticNetC
import time
from wrappers.glmnet import GlmnetWrapper
from sklearn.cross_validation import cross_val_score, KFold
from sklearn.metrics import make_scorer, mean_absolute_error
from sklearn.linear_model import SGDRegressor, Ridge, LogisticRegression, SGDClassifier, ElasticNet

MAD = make_scorer(mean_absolute_error, greater_is_better=False)

for ds in datasets.get_datasets():
    X, y = datasets.get_data(ds)
    kf = KFold(X.shape[0], 5, shuffle=True, random_state=1234)
    for a in (0.1, 0.3, 0.6, 0.9):
        for lm in (1, 0.1, 0.01, 0.001):
            if ds['rtype'] == 'Binary':
                continue
            if ds['rtype'] == 'Binary':
                clf1 = LogisticRegression()
                clf2 = ElasticNetC(distribution='Bernoulli', lambda_=lm, alpha=a, tolerance=0.0001)
                clf3 = SGDClassifier(alpha=lm, l1_ratio=a, loss='log', eta0=0.001, penalty='elasticnet')
                clf4 = GlmnetWrapper(**{'family': 'binomial', 'alpha': a, 'lambda': lm, 'maxit': 300})
                score_func = 'log_loss'
            else:
                clf1 = Ridge()
                clf2 = ElasticNetC(distribution='Gaussian', lambda_=lm, alpha=a, tolerance=0.001)
                clf3 = SGDRegressor(alpha=lm, l1_ratio=a, eta0=0.001, penalty='elasticnet')
                clf4 = GlmnetWrapper(**{'family': 'gaussian', 'alpha': a, 'lambda': lm, 'maxit': 300})
                clf5 = ElasticNet(l1_ratio=a, alpha=lm)
                score_func = MAD
            for clf in (clf1, clf2, clf3, clf4, clf5):
                if clf != clf1 or (a == 0.1 and lm == 1):
                    st = time.time()
                    print '%-20s %20s a %3.1f lm %8.4f sc %9.4f tm %5.2f' % \
                          (ds['name'], clf.__class__.__name__, a, lm,
                           cross_val_score(clf, X, y, cv=kf, scoring=score_func, n_jobs=3).mean(), time.time()-st)
