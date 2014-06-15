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
    v=1/(1+math.exp(-float(a[1])))
    pred['xgb'][a[0]]=v
    avg+=v
avg/=250000
sd=0
for v in pred['xgb'].values():
    sd += (v-avg)**2
sd=math.sqrt(sd/250000)
for k in pred['xgb'].keys():
    pred['xgb'][k] = (pred['xgb'][k]-avg)/sd

f=open('trainthg.csv','r') #
pred['thg']={}
avg=0
for l in f:
    a=l.rstrip().split(',')
    pred['thg'][a[0]]=float(a[1])
    avg+=float(a[1])
avg/=250000
sd=0
for v in pred['thg'].values():
    sd += (v-avg)**2
sd=math.sqrt(sd/250000)
for k in pred['thg'].keys():
    pred['thg'][k] = (pred['thg'][k]-avg)/sd

f=open('predxgbtr1000nw.csv','r')
pred['xgbnw']={}
avg=0
for l in f:
    a=l.rstrip().split(',')
    pred['xgbnw'][a[0]]=float(a[1])
    avg+=float(a[1])
avg/=250000
sd=0
for v in pred['xgbnw'].values():
    sd += (v-avg)**2
sd=math.sqrt(sd/250000)
for k in pred['xgbnw'].keys():
    pred['xgbnw'][k] = (pred['xgbnw'][k]-avg)/sd

#f=open('predlr1.csv','r') #3.086161
#f=open('predlr1l.csv','r') #3.219877
#f=open('predlr1lsw.csv','r') #3.231389
f=open('predlr1lsw2.csv','r') #3.244810
#f=open('predlr1d.csv','r') #1.5
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

#f=open('trainrgbmb1000_0.05_300_12.csv','r')
f=open('trainrgbmb2000_0.05_300_12.csv','r')
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

f=open('trainrgbmbs1000_0.05_300_12.csv','r')
h=f.readline()
pred['rgbmbs']={}
avg=0
for l in f:
    a=l.rstrip().split(',')
    pred['rgbmbs'][str(int(float(a[1])))]=float(a[2])
    avg+=float(a[2])
avg/=250000
sd=0
for v in pred['rgbmbs'].values():
    sd += (v-avg)**2
sd=math.sqrt(sd/250000)
for k in pred['rgbmbs'].keys():
    pred['rgbmbs'][k] = (pred['rgbmbs'][k]-avg)/sd

f=open('trainrgbmg_1000_0.05_300_12.csv','r')
#f=open('trainrgbmg_-0.5_1000_0.05_300_12.csv','r') #3.298684
#f=open('trainrgbmg_-1_1000_0.05_300_12.csv','r') #
h=f.readline()
pred['rgbmg']={}
pred['rgbmg2']={}
pred['rgbmgxb']={}
avg=0
avg1=0
for l in f:
    a=l.rstrip().split(',')
    #v=1/(1+float(a[2]))
    v=float(a[2])
    pred['rgbmg'][str(int(float(a[1])))]=v
    pred['rgbmg2'][str(int(float(a[1])))]=float(a[2])*float(a[2])
    pred['rgbmgxb'][str(int(float(a[1])))]=(10-pred['rgbmg'][str(int(float(a[1])))])*pred['rgbmb'][str(int(float(a[1])))]
    avg+=v
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
for v in pred['rgbmg2'].values():
    sd += (v-avg)**2
sd=math.sqrt(sd/250000)
for k in pred['rgbmg2'].keys():
    pred['rgbmg2'][k] = (pred['rgbmg2'][k]-avg)/sd
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

f=open('traintbb_200_5_500.csv','r') #
pred['tbb']={}
avg=0
for l in f:
    a=l.rstrip().split(',')
    pred['tbb'][str(int(float(a[0])))]=float(a[1])
    avg+=float(a[1])
avg/=250000
sd=0
for v in pred['tbb'].values():
    sd += (v-avg)**2
sd=math.sqrt(sd/250000)
for k in pred['tbb'].keys():
    pred['tbb'][k] = (pred['tbb'][k]-avg)/sd

f=open('trainrfw_1000_6_10_2.000000.csv','r') #
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

f=open('trainrfg_500_16_10.csv','r') #
pred['rfg']={}
avg=0
for l in f:
    a=l.rstrip().split(',')
    pred['rfg'][str(int(float(a[0])))]=float(a[1])
    avg+=float(a[1])
avg/=250000
sd=0
for v in pred['rfg'].values():
    sd += (v-avg)**2
sd=math.sqrt(sd/250000)
for k in pred['rfg'].keys():
    pred['rfg'][k] = (pred['rfg'][k]-avg)/sd

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
#f=open('predksvmc5','r') #
#f=open('train_ksvmc5.csv','r')
f=open('train_ksvmc10.csv','r') #
h=f.readline()
pred['svm10']={}
avg=0
for l in f:
    a=l.rstrip().split(',')
    pred['svm10'][str(int(float(a[1])))]=float(a[2])
    avg+=float(a[2])
avg/=250000
sd=0
for v in pred['svm10'].values():
    sd += (v-avg)**2
sd=math.sqrt(sd/250000)
for k in pred['svm10'].keys():
    pred['svm10'][k] = (pred['svm10'][k]-avg)/sd

f=open('train_ksvmc5.csv','r')
h=f.readline()
pred['svm5']={}
avg=0
for l in f:
    a=l.rstrip().split(',')
    pred['svm5'][str(int(float(a[1])))]=float(a[2])
    avg+=float(a[2])
avg/=250000
sd=0
for v in pred['svm5'].values():
    sd += (v-avg)**2
sd=math.sqrt(sd/250000)
for k in pred['svm5'].keys():
    pred['svm5'][k] = (pred['svm5'][k]-avg)/sd

#f=open('predbam.csv','r') #3.135016
f=open('train_gam_v1.csv','r') #
#f=open('train_gam012.csv','r') #
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

f=open('train_gam012.csv','r') #
h=f.readline()
pred['gamt']={}
avg=0
for l in f:
    a=l.rstrip().split(',')
    pred['gamt'][str(int(float(a[1])))]=float(a[2])
    avg+=float(a[2])
avg/=250000
sd=0
for v in pred['gamt'].values():
    sd += (v-avg)**2
sd=math.sqrt(sd/250000)
for k in pred['gamt'].keys():
    pred['gamt'][k] = (pred['gamt'][k]-avg)/sd

f=open('train_gam_ptw.csv','r') #
h=f.readline()
pred['gamtw']={}
avg=0
for l in f:
    a=l.rstrip().split(',')
    pred['gamtw'][str(int(float(a[1])))]=float(a[2])
    avg+=float(a[2])
avg/=250000
sd=0
for v in pred['gamtw'].values():
    sd += (v-avg)**2
sd=math.sqrt(sd/250000)
for k in pred['gamtw'].keys():
    pred['gamtw'][k] = (pred['gamtw'][k]-avg)/sd


f=open('trainrgbmpw_1000_0.05_300_12.csv','r') #
h=f.readline()
pred['rgbmpw']={}
avg=0
for l in f:
    a=l.rstrip().split(',')
    pred['rgbmpw'][str(int(float(a[1])))]=float(a[2])
    avg+=float(a[2])
avg/=250000
sd=0
for v in pred['rgbmpw'].values():
    sd += (v-avg)**2
sd=math.sqrt(sd/250000)
for k in pred['rgbmpw'].keys():
    pred['rgbmpw'][k] = (pred['rgbmpw'][k]-avg)/sd


f=open('training.csv','r')
l=f.readline()
wt={}
y={}
for l in f:
    a=l.rstrip().split(',')
    y[a[0]]=(1 if a[32]=='s' else 0)
    wt[a[0]]=float(a[31])

#use = ('xgb',) #3.593036
#use = ('xgb','gam') #3.594514
#use = ('xgb','gamt') #3.639165
#use = ('xgb','rgbmg') #3.633252
#use = ('xgb','svm') #3.642608
#use = ('xgb','rfbw') #3.644874
#use = ('xgb','rfbw') #3.662671
#use = ('xgb','rgbmb') #3.680602
#use = ('xgb','rgbmaw') #3.690853
#use = ('xgb','rgbmbw') #3.692947
#use = ('xgb','rgbmgxb') #3.694732
#use = ('xgb','rgbmg','rgbmb') #3.711947
#use = ('xgb','rgbmg','rgbmb','rgbmbs') #3.724860
#use = ('xgb','rgbmg','rgbmb','lr1') #
#use = ('xgb','rgbmg','rgbmb','tbb') #3.714670
#use = ('xgb','rgbmg','rgbmb','rfg') #3.710417
#use = ('xgb','rgbmg','rgbmb','rgbmgxb') #3.706690
#use = ('xgb','rgbmg','rgbmb','lr1') #3.708084
#use = ('xgb','rgbmg','rgbmb','rfbw') #3.713874
#use = ('xgb','rgbmg','rgbmb','rgbmaw') #3.715835
#use = ('xgb','rgbmg','rgbmb','rgbmbw') #3.717011
#use = ('xgb','rgbmg','rgbmb','gam') #3.727932
#use = ('xgb','rgbmg','rgbmb','gamt') #3.727932
#use = ('xgb','rgbmg','rgbmb','svm') #svm10 3.728037
#use = ('xgb','rgbmg','rgbmb','svm') #svm5
#use = ('xgb','rgbmg','rgbmb','svm','rgbmg2') #
#use = ('xgb','rgbmg','rgbmb','svm','rgbmgxb') #3.729710
#use = ('xgb','rgbmg','rgbmb','svm','xgbnw') #3.730067
#use = ('xgb','rgbmg','rgbmb','svm','rfbw') #3.731998
#use = ('xgb','rgbmg','rgbmb','svm','gam') #3.733050
#use = ('xgb','rgbmg','rgbmb','svm','rgbmbw') #3.743792
#use = ('xgb','rgbmg','rgbmb','svm','rgbmbw','rfbw') #3.742488
#use = ('xgb','rgbmg','rgbmb','svm','rgbmbw','gam') #3.752308
#use = ('xgb','rgbmg','rgbmb','svm','rgbmbw','gam','rgbmpw') #
#use = ('xgb','rgbmg','rgbmb','rgbmbw','rfbw','gam') #3.732072
#use = ('xgb','rgbmg','rgbmb','rgbmbw','rfbw','gam','gamt') #
#use = ('xgb','rgbmg','rgbmb','rgbmbw','rfbw','rgbmbs','gamt','svm') #
#use = ('xgb','rgbmg','rgbmb','svm','rgbmbw','rfbw','gam','rfg') #
#use = ('xgb','xgbnw','lr1','rgbmg','rgbmb','rgbmbs','svm','rgbmbw','rfbw','gam','gamt','gamtw','rfg','rgbmaw') #
#use = ('xgb','gamtw') #3.659174
#use = ('xgb','gamtw','gam') #3.660973
#use = ('xgb','gamtw','rgbmg') #3.669794
#use = ('xgb','gamtw','svm') #3.701167
#use = ('xgb','gamtw','rfbw') #3.703693
#use = ('xgb','gamtw','rgbmbw') #3.711876
#use = ('xgb','gamtw','rgbmbw','svm5') #3.707122
#use = ('xgb','gamtw','rgbmbw','rfbw') #3.714187
#use = ('xgb','gamtw','rgbmbw','svm10') #3.716219
#use = ('xgb','gamtw','rgbmbw','rgbmbs') #3.717437
#use = ('xgb','gamtw','rgbmbw','rgbmbs','rgbmb') #3.714
#use = ('xgb','gamtw','rgbmbw','rgbmbs','rgbmg') #3.721813
#use = ('xgb','gamtw','rgbmbw','rgbmbs','svm10') #3.726944
#use = ('xgb','gamtw','rgbmbw','rgbmbs','rfbw') #3.726931
#use = ('xgb','gamtw','rgbmbw','rgbmbs','rfbw','svm10') #3.726409
#use = ('xgb','gamtw','rgbmbw','rgbmbs','rfbw','rgbmg') #3.724429
use = ('xgb','gamtw','rgbmbw','rgbmbs','rfbw','svm10','rgbmg','gam') #

sys.stdout.write('y,wt')
for pk in use:
    sys.stdout.write(',%s' % pk)
sys.stdout.write('\n')

for ref in y.keys():
    sys.stdout.write("%s,%s" % (y[ref],wt[ref]))
    for pk in use:
        sys.stdout.write(',%f' % pred[pk][ref])
    sys.stdout.write('\n')
#ws = { 'xgb':0.582723, 'rgbmg': -0.354122, 'rgbmb': 0.284462, 'svm': 0.218808, 'rgbmbw': 0.350164, 'rfbw': 0.127386, 'gam': -0.209421 }
#print "EventId,LogOdds"
#for ref in y.keys():
#    p = 0
#    for k in pred.keys():
#        if k in ws:
#            p += ws[k]*pred[k][ref]
#    print '%s,%s' % (ref,p*wt[ref])
