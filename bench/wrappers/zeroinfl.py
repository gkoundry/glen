from sklearn.metrics import log_loss, mean_squared_error
import numpy as np
import rpy2.robjects as robjects
import rpy2.robjects.numpy2ri
rpy2.robjects.numpy2ri.activate()
from rpy2.robjects.numpy2ri import numpy2ri
robjects.conversion.py2ri = numpy2ri
from rpy2.robjects.packages import importr
pscl = importr("pscl")


class ZeroInflWrapper(object):
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
        #Y = np.reshape(Y, [-1, 1])
        robjects.globalenv['X'] = X
        robjects.globalenv['Y'] = Y-20
        data=robjects.r('data.frame(y=Y,X)')
        f=robjects.r('as.formula("y ~ .")')
        self.model = pscl.zeroinfl(f,data=data, **self.args)
        return self

    def predict(self, X):
        robjects.globalenv['X'] = X
        data=robjects.r('data.frame(X)')
        return np.array(pscl.predict_zeroinfl(self.model, data, type="response"))+20

