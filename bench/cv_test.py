import pandas
import numpy as np
from collections import defaultdict
from sklearn.metrics import r2_score

d = pandas.read_csv( '/home/glen/datasets/testdata/fastiron-train-30k.csv')

#x=d['ModelID']
x=d['fiModelDesc']
y=d['SalePrice']

for k in (0,): #,1,2,4,8,16,32,64,128):
    rows=np.arange(x.shape[0])
    np.random.seed(1234)
    np.random.shuffle(rows)
    l=x.shape[0]/2
    train = rows[:l]
    test = rows[l:]

    mu=defaultdict(float)
    cn=defaultdict(int)
    yt=0
    ct=0
    for i in train:
        mu[x[i]] += y[i]
        cn[x[i]] += 1
        yt += y[i]
        ct += 1

    pred = []
    for i in train:
        if x[i] in cn:
            xa=mu[x[i]]*1.0/cn[x[i]]
            bc=cn[x[i]]*1.0/(k+cn[x[i]])
            ya=yt*1.0/ct
            pred.append(bc*xa+(1-bc)*ya)
            print 'x='+str(x[i])+' yc='+str(mu[x[i]]/cn[x[i]])+' count='+str(cn[x[i]])
        else:
            pred.append(yt*1.0/ct)
    print '%d %f' % (k,r2_score(y[train],pred))
