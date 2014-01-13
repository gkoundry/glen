import sys
import numpy as np
sys.path.append('/home/glen/workspace')
from ModelingMachine.engine.tasks.ElasticNet import ElasticNet

class ElasticNetC(object):
    def __init__(self,**args):
        self.args=args
        self.clf=ElasticNet()

    def fit(self,X,y,**args):
        self.args.update(args)
        self.clf.fit(np.ascontiguousarray(X).astype(float),y.astype(float),path=False,**self.args)

    def predict(self,X):
        return self.clf.predict(np.ascontiguousarray(X).astype(float))

    def predict_proba(self,X):
        p = self.clf.predict(np.ascontiguousarray(X).astype(float))
        return np.column_stack((1-p, p))

    def set_params(self,**args):
        self.args.update(args)

    def get_params(self,deep=False):
        return self.args

