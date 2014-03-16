import pandas
import numpy as np
from collections import defaultdict
from sklearn.metrics import r2_score

d = pandas.read_csv( '/home/glen/datasets/testdata/kickcars_train_full.csv')
dt = pandas.read_csv( '/home/glen/datasets/testdata/kickcars_test.csv')

id=d['RefId']
x=d['ModelID']
#x=d['fiModelDesc']
y=d['SalePrice']

k=1

mu=defaultdict(float)
cn=defaultdict(int)
yt=0
ct=0
for i in d.shape[0]:
    mu[x[i]] += y[i]
    cn[x[i]] += 1
    yt += y[i]
    ct += 1

pred = []
print 'RefId,IsBadBuy'
for i in dt.shape[0]:
    if x[i] in cn:
        xa=mu[x[i]]*1.0/cn[x[i]]
        bc=cn[x[i]]*1.0/(k+cn[x[i]])
        ya=yt*1.0/ct
        pred = bc*xa+(1-bc)*ya
    else:
        pred = yt*1.0/ct
    print id[i]+','+str(pred)
