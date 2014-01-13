from sklearn.metrics import log_loss, mean_squared_error
import numpy as np
import rpy2.robjects as robjects
import rpy2.robjects.numpy2ri
rpy2.robjects.numpy2ri.activate()
from rpy2.robjects.numpy2ri import numpy2ri
robjects.conversion.py2ri = numpy2ri
from rpy2.robjects.packages import importr
glmnet = importr("glmnet")


class GlmnetWrapper(object):
    def __init__(self, **args):
        self.model = None
        self.args = args
        self.used_vars = []

    def score(self, X, act):
        pred = self.predict(X)
        if self.args['family'] == 'binomial':
            return log_loss(act, pred)
        else:
            return mean_squared_error(act, pred)

    def set_params(self, **args):
        self.args.update(args)
        return self

    def get_params(self, deep=True):
        return self.args

    def fit(self, X, Y, **args):
        self.args.update(args)
        self.model = glmnet.glmnet(X, np.reshape(Y, [-1, 1]), **self.args)
        return self

    def predict(self, X):
        return glmnet.predict_glmnet(self.model, X,
                                     **{'s': self.args['lambda'],
                                        'type': "response"})

    def predict_proba(self, X):
        p = glmnet.predict_glmnet(self.model, X, self.args['lambda'])
        p = 1/(1+np.exp(-np.array(p)))
        return np.column_stack((1-p, p))
