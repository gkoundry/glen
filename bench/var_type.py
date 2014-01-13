import datasets
import math
from wrappers.correlation import ace
import numpy as np
from collections import defaultdict

sc = defaultdict(int)
total = defaultdict(int)
for ds in datasets.get_datasets():
    print ds['name']
    Xc, yc = datasets.get_data(ds, convert='numbers', standardize=False)
    cat_cor = ace(Xc, yc, range(Xc.shape[1]), ds['rtype'])
    num_cor = ace(Xc, yc, [], ds['rtype'])
    for b in (0.4,0.5,0.6,0.7,0.8,0.85,0.9,0.95,1.0,1.1,1.2,1.3):
        for i,c in enumerate(datasets.get_columns(ds)):
            bias = len(np.unique(Xc[:,i]))*1.0/(b*Xc.shape[0])
            guess = 'num' if num_cor[i]>cat_cor[i]-bias else 'cat'
            if guess == 'cat' and i in datasets.get_column_index(ds) or guess == 'num' and i not in datasets.get_column_index(ds):
                sc[b] += 1
            total[b] += 1
            #print '%-30s %10.7f %10.7f %10.7f %s' % (c,num_cor[i],cat_cor[i],bias,guess)
        print '%6.2f %6.2f%%' % (b,sc[b]*100/total[b])
