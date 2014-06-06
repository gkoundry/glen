from GLM import GLM
import pandas
import random
import copy
import math
import numpy as np
import sys
from itertools import product

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
f=open('predxgbp.csv','r') #3.588919
pred['xgb']={}
pred['const']={}
for l in f:
    a=l.rstrip().split(',')
    pred['xgb'][a[0]]=float(a[1])
    pred['const'][a[0]]=1.0

#f=open('predlr1.csv','r') #3.086161
#f=open('predlr1l.csv','r') #3.219877
#f=open('predlr1lsw.csv','r') #3.231389
f=open('predlr1lsw2p.csv','r') #3.244810
pred['lr1']={}
for l in f:
    a=l.rstrip().split(',')
    pred['lr1'][a[0]]=float(a[1])

f=open('test.csv','r')
h=f.readline()
idt=[]
for l in f:
    a=l.split(',')
    idt.append(a[0])

f=open('testrgbmb1000_0.05_300_12.csv','r')
h=f.readline()
pred['rgbmb']={}
r=0
for l in f:
    a=l.rstrip().split(',')
    pred['rgbmb'][idt[r]]=float(a[1])
    r+=1

f=open('testrgbmg1000_0.05_300_12.csv','r') 
h=f.readline()
pred['rgbmg']={}
r=0
for l in f:
    a=l.rstrip().split(',')
    pred['rgbmg'][idt[r]]=float(a[1])
    r+=1

f=open('testrgbmbw1000_0.05_300_12.csv','r')
h=f.readline()
pred['rgbmbw']={}
r=0
for l in f:
    a=l.rstrip().split(',')
    pred['rgbmbw'][idt[r]]=float(a[1])
    r=r+1

##f=open('predksvm.csv','r') #3.135016
##f=open('predksvmc0p5.csv','r') #3.112735
#f=open('predksvmc5.csv','r') #3.112735
#h=f.readline()
#pred['svm']={}
#avg=0
#for l in f:
#    a=l.rstrip().split(',')
#    pred['svm'][str(int(float(a[1])))]=float(a[2])
#    avg+=float(a[2])
#avg/=250000
#sd=0
#for v in pred['svm'].values():
#    sd += (v-avg)**2
#sd=math.sqrt(sd/250000)
#for k in pred['svm'].keys():
#    pred['svm'][k] = (pred['svm'][k]-avg)/sd
#
#f=open('predbam.csv','r') #3.135016
#h=f.readline()
#pred['bam']={}
#avg=0
#for l in f:
#    a=l.rstrip().split(',')
#    pred['bam'][str(int(float(a[1])))]=float(a[2])
#    avg+=float(a[2])
#avg/=250000
#sd=0
#for v in pred['bam'].values():
#    sd += (v-avg)**2
#sd=math.sqrt(sd/250000)
#for k in pred['bam'].keys():
#    pred['bam'][k] = (pred['bam'][k]-avg)/sd

#f=open('training.csv','r')
#l=f.readline()
#wt={}
#y={}
#for l in f:
#    a=l.rstrip().split(',')
#    y[a[0]]=(1 if a[32]=='s' else 0)
#    wt[a[0]]=float(a[31])

#d=pandas.DataFrame({'y':[j for i,j in sorted(y.items(),key=lambda x:x[0])]})
#for a,v in pred.items():
#    d[a]=[j for i,j in sorted(v.items(),key=lambda x:x[0])]
#d.to_csv('blend1.out')
#yn = d.pop('y').values.astype(float)
#xn = np.ascontiguousarray(d.values).astype(float)
#m = GLM()
#m.fit(xn,yn,distribution='Bernoulli')
#print m.coef_
#bp = m.predict(xn)
#p1 = zip(sorted(y.keys()),bp.tolist())
#po = pandas.DataFrame({'id':[i[0] for i in sorted(p1,key=lambda x:x[1])],'rnk':range(1,len(p1)+1)})
#po.to_csv('test.out')
#sys.exit(0)
#ws= {'lr1':0.03,'svm': 0.048999999999999995, 'rgbmg': 0.146, 'rgbm': 0.316, 'xgb': 0.596} 
#ws= {'lr1':0.05, 'rgbm': 0.316, 'xgb': 0.596} 
#ws = {
#    'lr1': 0.00,
#    'svm': 0.00,
#    'rgbm': 0.4,
#    'rgbmg': 0.00,
#    'bam': 0.00,
#    'xgb': 0,
#}
ws={
    'const': 0,
    'xgb': 0.05,
    'rgbmb': 0.25,
    'rgbmg': 0.25,
    'rgbmbw': 0.25,
    'lr1':0,
}
ws = {'const': -0.06799999999999998, 'xgb': 0.3024, 'lr1': 0.052, 'rgbmg': -0.18589999999999998, 'rgbmbw': 0.04800000000000001, 'rgbmb': 0.14300000000000002} #0.760000 3.709946
th=0.760000 

pl=[]
for i,a in pred['const'].items():
    p = 0
    for k in pred.keys():
        if k in ws:
            p += ws[k]*pred[k][i]
    pl.append((i,p))

print 'EventId,RankOrder,Class'
r=1
pos=0
for i in sorted(pl,key=lambda x:-x[1]):
    print '%s,%s,%s' % (i[0],r,'s' if i[1]>th else 'b')
    if i[1]>th:
        pos+=1
    r+=1
sys.stderr.write('pos %f\n' % (pos/550000.0))
