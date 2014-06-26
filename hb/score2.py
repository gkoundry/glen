import numpy as np
import math
import random

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

pred={}
f=open('predxgb.csv','r') #3.593036070
#f=open('predxgbtr1000.csv','r') #3.6058075
pred['xgb']={}
for l in f:
    a=l.rstrip().split(',')
    v=1/(1+math.exp(-float(a[1])))
    pred['xgb'][int(a[0])]=v

f=open('trainrgbmbw1000_0.05_300_12.csv','r')
h=f.readline()
pred['rgbmbw']={}
for l in f:
    a=l.rstrip().split(',')
    pred['rgbmbw'][int(float(a[1]))]=float(a[2])

f=open('training.csv','r')
l=f.readline()
wt={}
y={}
for l in f:
    a=l.rstrip().split(',')
    y[int(a[0])]=(1 if a[32]=='s' else 0)
    wt[int(a[0])]=float(a[31])

random.seed(1234)
for l in range(50):
    pl=[]
    rc=0
    for i in y.keys():
        if random.randint(0,100)>60:
            pl.append([pred['rgbmbw'][i],y[i],wt[i]])
            rc+=1
    py=sorted(pl,key=lambda x:-x[0])
    sc=0
    bc=0
    best=0
    bestt=0
    for th in range(0,50000):
        if py[th][1]==1:
            sc+=py[th][2] * 250000/rc
        else:
            bc+=py[th][2] * 250000/rc
        ams=AMS(sc,bc)
        if ams>best:
            best=ams
            bestt=th
    print '%s %s %s' % (rc,best,bestt)
