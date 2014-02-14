import numpy as np
from scipy.stats import nanmedian
from ModelingMachine.engine.pandas_data_utils import pctParser,isPercentage,isDate,dateParser
import rpy2.robjects as robjects
from rpy2.robjects.numpy2ri import numpy2ri
robjects.conversion.py2ri = numpy2ri
import rpy2.robjects.numpy2ri
rpy2.robjects.numpy2ri.activate()
from rpy2.robjects.vectors import IntVector
from rpy2.robjects.packages import importr
acepack = importr("acepack")

def na_median(X):
    ''' returns a copy of X with NAs
    replaced by the median of the non NAs
    for each column
    '''
    col_median = nanmedian(X,axis=0)
    a=np.copy(X)
    inds = np.where(np.isnan(a))
    import sys
    sys.stderr.write(str(inds)+'\n')
    if inds[0].shape[0]>0:
        a[inds]=col_median
    return a

def ace(X,y,cats,rtype):
    corr = []
    if rtype=='C':
        cols=[0,]
    else:
        cols=[]
    if cats:
        rsq = acepack.ace(na_median(X), y, cat=IntVector(cols+[1,]))
    else:
        rsq = acepack.ace(na_median(X), y, cat=IntVector(cols))
    return rsq.rx2('rsq')[0]

def num_cat(x,y,c,t):
    if isDate(x):
        x = dateParser(x)
    cat_cor = ace(x, y, True, t)
    num_cor = ace(x, y, False, t)
    bias = len(np.unique(x))*1.0/(0.9*x.shape[0])
    guess = False if num_cor>cat_cor-bias else True
    return guess
