import sys
import math
import numpy as np
sys.path.append('/home/glen/workspace')
from ModelingMachine.engine.tasks.TreeBoost import TreeBoost as TreeBoostC

class TreeBoost(object):
    def __init__(self,**args):
        self.args=args
        self.clf=TreeBoostC()

    def fit(self,X,y,**args):
        self.args.update(args)
        if self.args['mtry']=='auto':
            self.args['mtry']=int(math.sqrt(X.shape[1]))
        self.clf.fit(np.ascontiguousarray(X).astype(float),y.astype(float),**self.args)

    def predict(self,X):
        return self.clf.predict(np.ascontiguousarray(X).astype(float))

    def predict_proba(self,X):
        p = np.array(self.clf.predict(np.ascontiguousarray(X).astype(float)))
        return np.column_stack((1-p, p))

    def set_params(self,**args):
        self.args.update(args)

    def get_params(self,deep=False):
        return self.args

