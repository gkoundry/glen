import sys
import numpy as np
import scipy as sp
#sys.path.append('/home/glen/workspace')
#from ModelingMachine.engine.tasks.ElasticNet import ElasticNet
from ElasticNet import ElasticNet

class ElasticNetC(object):
    def __init__(self,**args):
        self.args=args
        self.clf=ElasticNet()

    def fit(self,X,y,**args):
        self.args.update(args)
        if sp.sparse.issparse(X):
            self.clf.fit(X.tocsc().astype(float),y.astype(float),path=False,**self.args)
        else:
            self.clf.fit(np.ascontiguousarray(X).astype(float),y.astype(float),path=False,**self.args)
        self.coef_ = self.clf.coef_

    def predict(self,X):
        if sp.sparse.issparse(X):
            return self.clf.predict(X.tocsc().astype(float))
        else:
            return self.clf.predict(np.ascontiguousarray(X).astype(float))

    def predict_proba(self,X):
        if sp.sparse.issparse(X):
            p = self.clf.predict(X.tocsc().astype(float))
        else:
            p = self.clf.predict(np.ascontiguousarray(X).astype(float))
        return np.column_stack((1-p, p))

    def set_params(self,**args):
        self.args.update(args)

    def get_params(self,deep=False):
        return self.args

