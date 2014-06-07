from copy import copy
import numpy as np
import pandas
import math

def AMS(s, b):
    """ Approximate Median Significance defined as:
        AMS = sqrt(
                2 { (s + b + b_r) log[1 + (s/(b+b_r))] - s}
              )
    where b_r = 10, b = background, s = signal, log is natural logarithm """

    br = 10.0
    radicand = 2 *( (s+b+br) * math.log (1.0 + s/(b+br)) -s)
    if radicand < 0:
        print 'radicand is negative. Exiting'
        exit()
    else:
        return math.sqrt(radicand)

d=pandas.read_csv('vote.csv')
y=d.pop('y')
wt=d.pop('wt')
cols = d.shape[1]
b=[1.0/cols]*cols
while True:
    oldb=copy(b)
    for th in np.arange(0.4,0.9,0.01):
        sc=0
        bc=0
        for i,r in enumerate(d.iterrows()):
            pred = sum(np.array(b) * r[1].values)/sum(b)
            if pred>th:
                if y[i]==1:
                    sc+=wt[i]
                else:
                    bc+=wt[i]
        print '%f %f %f %f' % (sc,bc,th,AMS(sc,bc))
    cc = (cc + 1) % cols
