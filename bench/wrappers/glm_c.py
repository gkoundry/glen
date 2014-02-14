import sys
import numpy as np
from GLM import GLM

class CGLM(object):
    def __init__(self,**args):
        self.args=args
        self.clf=GLM()

    def fit(self,X,y,**args):
        self.args.update(args)
        self.clf.fit(np.ascontiguousarray(X).astype(float),y.astype(float),**self.args)

    def predict(self,X):
        return self.clf.predict(np.ascontiguousarray(X).astype(float))

    def predict_proba(self,X):
        p = self.clf.predict(np.ascontiguousarray(X).astype(float))
        return np.column_stack((1-p, p))

    def set_params(self,**args):
        self.args.update(args)

    def get_params(self,deep=False):
        return self.args

