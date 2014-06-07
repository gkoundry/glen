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
f=open('predxgb.csv','r') #3.588919
pred['xgb']={}
avg=0
for l in f:
    a=l.rstrip().split(',')
    pred['xgb'][a[0]]=float(a[1])
    avg+=float(a[1])
avg/=250000
sd=0
for v in pred['xgb'].values():
    sd += (v-avg)**2
sd=math.sqrt(sd/250000)
for k in pred['xgb'].keys():
    pred['xgb'][k] = (pred['xgb'][k]-avg)/sd

#f=open('predlr1.csv','r') #3.086161
#f=open('predlr1l.csv','r') #3.219877
#f=open('predlr1lsw.csv','r') #3.231389
f=open('predlr1lsw2.csv','r') #3.244810
pred['lr1']={}
avg=0
for l in f:
    a=l.rstrip().split(',')
    pred['lr1'][a[0]]=float(a[1])
    avg+=float(a[1])
avg/=250000
sd=0
for v in pred['lr1'].values():
    sd += (v-avg)**2
sd=math.sqrt(sd/250000)
for k in pred['lr1'].keys():
    pred['lr1'][k] = (pred['lr1'][k]-avg)/sd

#f=open('predrgbm_200_0.100000.csv','r') #3.454425
#f=open('predrgbm_400.csv','r') #3.403357
#f=open('predrgbm_300_0.100000_200.csv','r') #3.480559
#f=open('predrgbm_500_0.100000_200.csv','r') #3.508642
#f=open('predrgbm_t300_mn500_mf7_lr0p1.csv','r') #3.510688
#f=open('predrgbm_t300_mn500_mf7_lr0p1w2.csv','r') # 3.526620
#f=open('predrgbm_t300_mn500_mf7_lr0p1w6.csv','r') #3.518476
#f=open('predrgbm_t300_mn500_mf7_lr0p1w4.csv','r') #3.545303
#f=open('predrgbm_t300_mn500_mf7_lr0p1w4cv5.csv','r') #3.566532
#f=open('predrgbm_t300_mn500_mf7_lr0p1w4cv5c.csv','r') #3.561423
f=open('predrgbm_t200_mn500_mf18_lr0p1w4cv3c.csv','r')
h=f.readline()
pred['rgbm']={}
avg=0
for l in f:
    a=l.rstrip().split(',')
    pred['rgbm'][str(int(float(a[1])))]=float(a[2])
    avg+=float(a[2])
avg/=250000
sd=0
for v in pred['rgbm'].values():
    sd += (v-avg)**2
sd=math.sqrt(sd/250000)
for k in pred['rgbm'].keys():
    pred['rgbm'][k] = (pred['rgbm'][k]-avg)/sd

#f=open('predrgbmg_t300.csv','r') #2.662905
f=open('predrgbmgr.csv','r') 
h=f.readline()
pred['rgbmg']={}
avg=0
for l in f:
    a=l.rstrip().split(',')
    pred['rgbmg'][str(int(float(a[1])))]=float(a[2])
    avg+=float(a[2])
avg/=250000
sd=0
for v in pred['rgbmg'].values():
    sd += (v-avg)**2
sd=math.sqrt(sd/250000)
for k in pred['rgbmg'].keys():
    pred['rgbmg'][k] = (pred['rgbmg'][k]-avg)/sd

#f=open('predksvm.csv','r') #3.135016
#f=open('predksvmc0p5.csv','r') #3.112735
f=open('predksvmc5.csv','r') #3.112735
h=f.readline()
pred['svm']={}
avg=0
for l in f:
    a=l.rstrip().split(',')
    pred['svm'][str(int(float(a[1])))]=float(a[2])
    avg+=float(a[2])
avg/=250000
sd=0
for v in pred['svm'].values():
    sd += (v-avg)**2
sd=math.sqrt(sd/250000)
for k in pred['svm'].keys():
    pred['svm'][k] = (pred['svm'][k]-avg)/sd

f=open('predbam.csv','r') #3.135016
h=f.readline()
pred['bam']={}
avg=0
for l in f:
    a=l.rstrip().split(',')
    pred['bam'][str(int(float(a[1])))]=float(a[2])
    avg+=float(a[2])
avg/=250000
sd=0
for v in pred['bam'].values():
    sd += (v-avg)**2
sd=math.sqrt(sd/250000)
for k in pred['bam'].keys():
    pred['bam'][k] = (pred['bam'][k]-avg)/sd

f=open('training.csv','r')
l=f.readline()
wt={}
y={}
for l in f:
    a=l.rstrip().split(',')
    y[a[0]]=(1 if a[32]=='s' else 0)
    wt[a[0]]=float(a[31])

d=pandas.DataFrame({'y':[j for i,j in sorted(y.items(),key=lambda x:x[0])]})
for a,v in pred.items():
    d[a]=[j for i,j in sorted(v.items(),key=lambda x:x[0])]
#d.to_csv('blend1.out')
yn = d.pop('y').values.astype(float)
xn = np.ascontiguousarray(d.values).astype(float)
m = GLM()
m.fit(xn,yn,distribution='Bernoulli')
print m.coef_
bp = m.predict(xn)
#p1 = zip(sorted(y.keys()),bp.tolist())
#po = pandas.DataFrame({'id':[i[0] for i in sorted(p1,key=lambda x:x[1])],'rnk':range(1,len(p1)+1)})
#po.to_csv('test.out')
#sys.exit(0)
#ws= {'lr1':0.03,'svm': 0.048999999999999995, 'rgbmg': 0.146, 'rgbm': 0.316, 'xgb': 0.596} 
ws= {'lr1':0.05, 'rgbm': 0.316, 'xgb': 0.596} 
#ws = {
#    'lr1': 0.00,
#    'svm': 0.00,
#    'rgbm': 0.4,
#    'rgbmg': 0.00,
#    'bam': 0.00,
#    'xgb': 0,
#}

bestams=0
while True:
    for al in ws.keys():
        for inc in (-1,1):
            if al=='xgb':
                continue
            oldws=copy.copy(ws)
            ws[al] += inc * random.randint(10,100)/1000.0
            bestth=0
            bestsc=0
            ws['xgb']=1
            for i,j in ws.items():
                if i!='xgb':
                    ws['xgb'] -= j
            for th in np.arange(1.0,1.3,0.02):
                s=0
                b=0
                for i,a in y.items():
                    p = 0
                    for k in pred.keys():
                        if k in ws:
                            p += ws[k]*pred[k][i]
                    if p>th:
                        if a==1:
                            s+=wt[i]
                        else:
                            b+=wt[i]
                sc = AMS(s,b)
                if sc > bestsc:
                    bestsc=sc
                    bestth=th
            print '%s %f %f' % (['%s %5.3f' % (i,j) for i,j in ws.items()],bestth,bestsc)
            if bestsc>bestams:
                print '=====> %s %f %f' % (ws,bestth,bestsc)
                bestams=bestsc
            else:
                ws=oldws
            sys.stdout.flush()
