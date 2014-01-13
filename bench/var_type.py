import datasets
import math
from wrappers.correlation import ace
import numpy as np

for ds in datasets.get_datasets():
    Xc, yc = datasets.get_data(ds, convert='numbers', standardize=False)
    cat_cor = ace(Xc, yc, range(Xc.shape[1]))
    num_cor = ace(Xc, yc, [])
    for i,c in enumerate(datasets.get_columns(ds)):
        bias = len(np.unique(Xc[:,i]))/(1.386*Xc.shape[0])
        print '%-30s %10.7f %10.7f %10.7f %s' % (c,num_cor[i],cat_cor[i],bias,'num' if num_cor[i]>cat_cor[i]-1.5*bias else 'cat')
