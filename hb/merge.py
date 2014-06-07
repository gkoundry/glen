import pandas
import random
import copy
import math
import numpy as np
import sys
from itertools import product


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

f=open('trainrfw_200_15_10.csv','r') #3.484283
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

sys.stdout.write('y,wt')
for pk in sorted(pred.keys()):
    sys.stdout.write(',%s' % pk)
sys.stdout.write('\n')

for ref in y.keys():
    sys.stdout.write("%s,%s" % (y[ref],wt[ref]))
    for pk in sorted(pred.keys()):
        sys.stdout.write(',%f' % pred[pk][ref])
    sys.stdout.write('\n')
