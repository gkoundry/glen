from GLM import GLM
from scipy.optimize import fmin,fmin_powell,fmin_cobyla,anneal,basinhopping
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
pred['const']={}
avg=0
for l in f:
    a=l.rstrip().split(',')
    pred['xgb'][a[0]]=float(a[1])
    pred['const'][a[0]]=1.0
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

f=open('trainrgbmb1000_0.05_300_12.csv','r')
h=f.readline()
pred['rgbmb']={}
avg=0
for l in f:
    a=l.rstrip().split(',')
    pred['rgbmb'][str(int(float(a[1])))]=float(a[2])
    avg+=float(a[2])
avg/=250000
sd=0
for v in pred['rgbmb'].values():
    sd += (v-avg)**2
sd=math.sqrt(sd/250000)
for k in pred['rgbmb'].keys():
    pred['rgbmb'][k] = (pred['rgbmb'][k]-avg)/sd

f=open('trainrgbmg_1000_0.05_300_12.csv','r') 
#f=open('trainrgbmg_-0.5_1000_0.05_300_12.csv','r') #3.298684
#f=open('trainrgbmg_-1_1000_0.05_300_12.csv','r') #
h=f.readline()
pred['rgbmg']={}
pred['rgbmgxb']={}
avg=0
avg1=0
for l in f:
    a=l.rstrip().split(',')
    pred['rgbmg'][str(int(float(a[1])))]=float(a[2])
    pred['rgbmgxb'][str(int(float(a[1])))]=(10-pred['rgbmg'][str(int(float(a[1])))])*pred['rgbmb'][str(int(float(a[1])))]
    avg+=float(a[2])
    avg1+=pred['rgbmgxb'][str(int(float(a[1])))]
avg/=250000
avg1/=250000
sd=0
sd1=0
for v in pred['rgbmg'].values():
    sd += (v-avg)**2
sd=math.sqrt(sd/250000)
for k in pred['rgbmg'].keys():
    pred['rgbmg'][k] = (pred['rgbmg'][k]-avg)/sd
for v in pred['rgbmgxb'].values():
    sd1 += (v-avg1)**2
sd1=math.sqrt(sd1/250000)
for k in pred['rgbmgxb'].keys():
    pred['rgbmgxb'][k] = (pred['rgbmgxb'][k]-avg1)/sd1


f=open('trainrgbmbw1000_0.05_300_12.csv','r')
h=f.readline()
pred['rgbmbw']={}
avg=0
for l in f:
    a=l.rstrip().split(',')
    pred['rgbmbw'][str(int(float(a[1])))]=float(a[2])
    avg+=float(a[2])
avg/=250000
sd=0
for v in pred['rgbmbw'].values():
    sd += (v-avg)**2
sd=math.sqrt(sd/250000)
for k in pred['rgbmbw'].keys():
    pred['rgbmbw'][k] = (pred['rgbmbw'][k]-avg)/sd

f=open('trainrgbmaw1000_0.05_300_12.csv','r')
h=f.readline()
pred['rgbmaw']={}
avg=0
for l in f:
    a=l.rstrip().split(',')
    pred['rgbmaw'][str(int(float(a[1])))]=float(a[2])
    avg+=float(a[2])
avg/=250000
sd=0
for v in pred['rgbmaw'].values():
    sd += (v-avg)**2
sd=math.sqrt(sd/250000)
for k in pred['rgbmaw'].keys():
    pred['rgbmaw'][k] = (pred['rgbmaw'][k]-avg)/sd

#f=open('predksvm.csv','r') #3.135016
#f=open('predksvmc0p5.csv','r') #3.112735
f=open('predksvmc5.csv','r') #3.213296
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
#ws={
#    'const': 0,
#    'xgb': 0.05,
#    'rgbmb': 0.25,
#    'rgbmg': 0.25,
#    'rgbmbw': 0.25,
#    'lr1':0,
#}
#ws = {'lr1': 0.0478, 'const': -0.06609999999999998, 'rgbmg': -0.18589999999999998, 'rgbmaw': 0.01, 'rgbmbw': 0.0534, 'xgb': 0.3052, 'rgbmb': 0.1373} #0.760000 3.715434
#ws = {'rgbmaw': 0.017300000000000003, 'svm': 0.0422, 'const': -0.07649999999999997, 'xgb': 0.31949999999999995, 'lr1': 0.031700000000000006, 'rgbmg': -0.1883, 'rgbmbw': 0.0611, 'rgbmb': 0.14070000000000002} #0.840000 3.723809
#ws = {'rgbmaw': 0.023400000000000004, 'svm': 0.038900000000000004, 'const': -0.11239999999999996, 'xgb': 0.32119999999999993, 'lr1': -0.006799999999999994, 'rgbmg': -0.2045, 'rgbmbw': 0.0519, 'rgbmb': 0.13940000000000002} #0.780000 3.733511
#ws = {'rgbmaw': 0.051800000000000006, 'svm': 0.0779, 'const': -0.11239999999999996, 'xgb': 0.31639999999999996, 'lr1': -0.0021999999999999936, 'rgbmg': -0.2045, 'rgbmbw': 0.0873, 'rgbmb': 0.13940000000000002} #0.940000 3.721149
#ws = {'rgbmgxb': 0.05, 'xgb': 0.31639999999999996, 'rgbmg': -0.2045, 'rgbmb': 0.33940000000000002} #0.940000 3.721149
#ws = {'rgbmg': -0.2253, 'xgb': 0.3349, 'rgbmb': 0.22000000000000003} #0.900000 3.697358
ws =  {'rgbmxb':0, 'rgbmg': -0.1537, 'xgb': 0.3596999999999999, 'rgbmb': 0.24810000000000001} #0.900000 3.702030

bestams=0
bestth=0.9
while True:
    oldws=copy.copy(ws)
    if bestams!=0:
        for al in ws.keys():
            ws[al] += (random.randint(0,200)-100)/10000.0
    bestsc=0
    for th in np.arange(bestth-0.2,bestth+0.2,0.01):
        s=0
        b=0
        pos=0
        for i,a in y.items():
            p = 0
            for k in pred.keys():
                if k in ws:
                    p += ws[k]*pred[k][i]
            if p>th:
                pos+=1
                if a==1:
                    s+=wt[i]
                else:
                    b+=wt[i]
        sc = AMS(s,b)
        if sc > bestsc:
            bestsc=sc
            bestth=th
    print '%s %f %f %f' % (['%s %5.3f' % (i,j) for i,j in ws.items()],bestth,bestsc,pos/250000.0)
    if bestsc>bestams:
        print '=====> %s %f %f' % (ws,bestth,bestsc)
        bestams=bestsc
    else:
        ws=oldws
    sys.stdout.flush()

#x0 = [ 0.0478, -0.06609999999999998, -0.18589999999999998,  0.01,  0.0534, 0.3052,  0.1373]
#def func(a):
#    ws={}
#    (ws['lr1'],ws['const'],ws['rgbmg'],ws['rgbmaw'],ws['rgbmbw'],ws['xgb'],ws['rgbmb'])=a
#    bestsc=0
#    bestth=0
#    for th in np.arange(0.50,0.85,0.02):
#        s=0
#        b=0
#        pos=0
#        for i,a in y.items():
#            p = 0
#            for k in pred.keys():
#                if k in ws:
#                    p += ws[k]*pred[k][i]
#            if p>th:
#                pos+=1
#                if a==1:
#                    s+=wt[i]
#                else:
#                    b+=wt[i]
#        sc = AMS(s,b)
#        if sc > bestsc:
#            bestsc=sc
#            bestth=th
#    return -bestsc
#
#def cb(x):
#    print x
#print 'fmin_powell'
#print fmin_powell(func,x0)
