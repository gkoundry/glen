import rpy2.robjects as robjects
from rpy2.robjects.numpy2ri import numpy2ri
robjects.conversion.py2ri = numpy2ri
import rpy2.robjects.numpy2ri
rpy2.robjects.numpy2ri.activate()
from rpy2.robjects.vectors import IntVector
from rpy2.robjects.packages import importr
acepack = importr("acepack")
Hmisc = importr("Hmisc")
energy = importr("energy")

def ace(X,y,cats):
    corr = []
    for i,col in enumerate(X.T):
        if i in cats:
            rsq = acepack.ace(col, y, cat=IntVector([0, 1]))
        else:
            rsq = acepack.ace(col, y, cat=IntVector([0,]))
        corr.append(rsq.rx2('rsq')[0])
    return corr

def rcorrs(X, y, cats, ctype='spearman'):
    corr = []
    for i,col in enumerate(X.T):
        rsq = Hmisc.rcorr(col, y, **{'type': ctype})
        corr.append(abs(rsq[0][1]))
    return corr

def rcorrp(X, y, cats):
    return rcorrs(X, y, cats, ctype='pearson')

def bcdcor(X, y, cats):
    corr = []
    for i,col in enumerate(X.T):
        rsq = energy.dcor(col, y)
        print rsq[0]
        corr.append(abs(rsq[0]))
    return corr

