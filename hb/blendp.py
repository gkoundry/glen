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
avg=0
pred['xgb']={}
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
f=open('predlr1lsw2p.csv','r') #3.244810
avg=0
pred['lr1']={}
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

f=open('test.csv','r')
avg=0
h=f.readline()
idt=[]
for l in f:
    a=l.split(',')
    idt.append(a[0])

f=open('testrgbmb1000_0.05_300_12.csv','r')
avg=0
h=f.readline()
pred['rgbmb']={}
r=0
for l in f:
    a=l.rstrip().split(',')
    pred['rgbmb'][idt[r]]=float(a[1])
    avg+=float(a[1])
    r+=1
avg/=250000
sd=0
for v in pred['rgbmb'].values():
    sd += (v-avg)**2
sd=math.sqrt(sd/250000)
for k in pred['rgbmb'].keys():
    pred['rgbmb'][k] = (pred['rgbmb'][k]-avg)/sd

f=open('testrgbmg1000_0.05_300_12.csv','r')
avg=0
h=f.readline()
pred['rgbmg']={}
r=0
for l in f:
    a=l.rstrip().split(',')
    pred['rgbmg'][idt[r]]=float(a[1])
    avg+=float(a[1])
    r+=1
avg/=250000
sd=0
for v in pred['rgbmg'].values():
    sd += (v-avg)**2
sd=math.sqrt(sd/250000)
for k in pred['rgbmg'].keys():
    pred['rgbmg'][k] = (pred['rgbmg'][k]-avg)/sd

f=open('testrgbmbw1000_0.05_300_12.csv','r')
avg=0
h=f.readline()
pred['rgbmbw']={}
r=0
for l in f:
    a=l.rstrip().split(',')
    pred['rgbmbw'][idt[r]]=float(a[1])
    avg+=float(a[1])
    r=r+1
avg/=250000
sd=0
for v in pred['rgbmbw'].values():
    sd += (v-avg)**2
sd=math.sqrt(sd/250000)
for k in pred['rgbmbw'].keys():
    pred['rgbmbw'][k] = (pred['rgbmbw'][k]-avg)/sd

f=open('testrfw_1000_6_10_2.000000.csv','r') #
pred['rfbw']={}
avg=0
for l in f:
    a=l.rstrip().split(',')
    pred['rfbw'][str(int(float(a[0])))]=float(a[1])
    avg+=float(a[1])
avg/=250000
sd=0
for v in pred['rfbw'].values():
    sd += (v-avg)**2
sd=math.sqrt(sd/250000)
for k in pred['rfbw'].keys():
    pred['rfbw'][k] = (pred['rfbw'][k]-avg)/sd


##f=open('predksvm.csv','r') #3.135016
##f=open('predksvmc0p5.csv','r') #3.112735
#f=open('predksvmc5.csv','r') #3.112735
f=open('testsvmc5.csv','r')
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

#f=open('predbam.csv','r') #3.135016
f=open('test_gam_v1.csv','r') #
h=f.readline()
pred['gam']={}
avg=0
for l in f:
    a=l.rstrip().split(',')
    pred['gam'][str(int(float(a[1])))]=float(a[2])
    avg+=float(a[2])
avg/=250000
sd=0
for v in pred['gam'].values():
    sd += (v-avg)**2
sd=math.sqrt(sd/250000)
for k in pred['gam'].keys():
    pred['gam'][k] = (pred['gam'][k]-avg)/sd

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
#ws = { 'xgb': 0.3024, 'lr1': 0.052, 'rgbmg': -0.18589999999999998, 'rgbmbw': 0.04800000000000001, 'rgbmb': 0.14300000000000002} #0.760000 3.709946
#ws = {'xgb': 1.808217, 'rgbmg': -1.369249, 'rgbmb': 1.623148, 'svm':  0.465914, 'rgbmbw': 0.328718, 'rfbw': 0.428909, 'gam': -0.548600 }
ws = {'xgb': 1.547173, 'rgbmg': -1.039914, 'rgbmb': 1.275528, 'rgbmbw': 0.467442, 'rfbw': 0.403140, 'gam': -0.403513 }
th=0.760000

pl=[]
for i,a in pred['xgb'].items():
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
