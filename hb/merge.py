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

def maxAMS(pred,wt,y):
    bestsc=0
    bestth=0
    for th in np.linspace(np.percentile(pred,30),np.percentile(pred,95),150):
        i=0
        sc = 0
        bc = 0
        i=0
        for p in pred:
            if p>th:
                if y[i]==1:
                    sc += wt[i]
                else:
                    bc += wt[i]
            i += 1
        ams = AMS(sc,bc)
        if ams>bestsc:
            bestsc=ams
            bestth=th
    return (bestsc,bestth)
def iqr(a):
    return np.percentile(a.values(),90)-np.percentile(a.values(),10)

pred={}
sds={}
avgs={}

f=open('predxgb.csv','r') #3.588919
pred['xgb']={}
for l in f:
    a=l.rstrip().split(',')
    v=1/(1+math.exp(-float(a[1])))
    pred['xgb'][a[0]]=v
sds['xgb'] = iqr(pred['xgb'])
avgs['xgb'] = np.median(pred['xgb'].values())

f=open('trainthg.csv','r') #
pred['thg']={}
for l in f:
    a=l.rstrip().split(',')
    pred['thg'][a[0]]=float(a[1])
sds['thg'] = iqr(pred['thg'])
avgs['thg'] = np.median(pred['thg'].values())

f=open('predxgbtr1000nw.csv','r')
pred['xgbnw']={}
for l in f:
    a=l.rstrip().split(',')
    pred['xgbnw'][a[0]]=float(a[1])
sds['xgbnw'] = iqr(pred['xgbnw'])
avgs['xgbnw'] = np.median(pred['xgbnw'].values())

#f=open('predlr1.csv','r') #3.086161
#f=open('predlr1l.csv','r') #3.219877
#f=open('predlr1lsw.csv','r') #3.231389
f=open('predlr1lsw2.csv','r') #3.244810
#f=open('predlr1d.csv','r') #1.5
pred['lr1']={}
for l in f:
    a=l.rstrip().split(',')
    pred['lr1'][a[0]]=float(a[1])
sds['lr1'] = iqr(pred['lr1'])
avgs['lr1'] = np.median(pred['lr1'].values())

f=open('trainrgbmb1000_0.05_300_12.csv','r')
#f=open('trainrgbmb2000_0.05_300_12.csv','r')
h=f.readline()
pred['rgbmb']={}
for l in f:
    a=l.rstrip().split(',')
    pred['rgbmb'][str(int(float(a[1])))]=float(a[2])
sds['rgbmb'] = iqr(pred['rgbmb'])
avgs['rgbmb'] = np.median(pred['rgbmb'].values())

f=open('trainrgbmbs1000_0.05_300_12.csv','r')
h=f.readline()
pred['rgbmbs']={}
for l in f:
    a=l.rstrip().split(',')
    pred['rgbmbs'][str(int(float(a[1])))]=float(a[2])
sds['rgbmbs'] = iqr(pred['rgbmbs'])
avgs['rgbmbs'] = np.median(pred['rgbmbs'].values())

f=open('trainrgbmg_1000_0.05_300_12.csv','r')
#f=open('trainrgbmg_-0.5_1000_0.05_300_12.csv','r') #3.298684
#f=open('trainrgbmg_-1_1000_0.05_300_12.csv','r') #
h=f.readline()
pred['rgbmg']={}
pred['rgbmg2']={}
pred['rgbmgxb']={}
for l in f:
    a=l.rstrip().split(',')
    #v=1/(1+float(a[2]))
    v=float(a[2])
    pred['rgbmg'][str(int(float(a[1])))]=v
    pred['rgbmg2'][str(int(float(a[1])))]=float(a[2])*float(a[2])
    pred['rgbmgxb'][str(int(float(a[1])))]=(10-pred['rgbmg'][str(int(float(a[1])))])*pred['rgbmb'][str(int(float(a[1])))]
sds['rgbmg'] = iqr(pred['rgbmg'])
avgs['rgbmg'] = np.median(pred['rgbmg'].values())
sds['rgbmg2'] = iqr(pred['rgbmg2'])
avgs['rgbmg2'] = np.median(pred['rgbmg2'].values())
sds['rgbmgxb'] = iqr(pred['rgbmgxb'])
avgs['rgbmgxb'] = np.median(pred['rgbmgxb'].values())

f=open('trainrgbmbw1000_0.05_300_12.csv','r')
h=f.readline()
pred['rgbmbw']={}
for l in f:
    a=l.rstrip().split(',')
    pred['rgbmbw'][str(int(float(a[1])))]=float(a[2])
sds['rgbmbw'] = iqr(pred['rgbmbw'])
avgs['rgbmbw'] = np.median(pred['rgbmbw'].values())

f=open('traintbb_200_5_500.csv','r') #
pred['tbb']={}
for l in f:
    a=l.rstrip().split(',')
    pred['tbb'][str(int(float(a[0])))]=float(a[1])
sds['tbb'] = iqr(pred['tbb'])
avgs['tbb'] = np.median(pred['tbb'].values())

f=open('trainrfw_1000_6_10_2.000000.csv','r') #
#f=open('trainrfwt_1000_6_10_2.000000.csv','r') #
pred['rfbw']={}
for l in f:
    a=l.rstrip().split(',')
    pred['rfbw'][str(int(float(a[0])))]=float(a[1])
sds['rfbw'] = iqr(pred['rfbw'])
avgs['rfbw'] = np.median(pred['rfbw'].values())

f=open('trainrfg_500_16_10.csv','r') #
pred['rfg']={}
for l in f:
    a=l.rstrip().split(',')
    pred['rfg'][str(int(float(a[0])))]=float(a[1])
sds['rfg'] = iqr(pred['rfg'])
avgs['rfg'] = np.median(pred['rfg'].values())

f=open('trainrgbmaw1000_0.05_300_12.csv','r')
h=f.readline()
pred['rgbmaw']={}
for l in f:
    a=l.rstrip().split(',')
    pred['rgbmaw'][str(int(float(a[1])))]=float(a[2])
sds['rgbmaw'] = iqr(pred['rgbmaw'])
avgs['rgbmaw'] = np.median(pred['rgbmaw'].values())

#f=open('predksvm.csv','r') #3.135016
#f=open('predksvmc0p5.csv','r') #3.112735
#f=open('predksvmc5','r') #
#f=open('train_ksvmc5.csv','r')
f=open('train_ksvmc50.csv','r') #
h=f.readline()
pred['svm50']={}
for l in f:
    a=l.rstrip().split(',')
    pred['svm50'][str(int(float(a[1])))]=float(a[2])
sds['svm50'] = iqr(pred['svm50'])
avgs['svm50'] = np.median(pred['svm50'].values())

f=open('train_ksvmc10.csv','r') #
h=f.readline()
pred['svm10']={}
for l in f:
    a=l.rstrip().split(',')
    pred['svm10'][str(int(float(a[1])))]=float(a[2])
sds['svm10'] = iqr(pred['svm10'])
avgs['svm10'] = np.median(pred['svm10'].values())

f=open('train_ksvmc5.csv','r')
h=f.readline()
pred['svm5']={}
for l in f:
    a=l.rstrip().split(',')
    pred['svm5'][str(int(float(a[1])))]=float(a[2])
sds['svm5'] = iqr(pred['svm5'])
avgs['svm5'] = np.median(pred['svm5'].values())

#f=open('predbam.csv','r') #3.135016
f=open('train_gam_v1.csv','r') #
#f=open('train_gam012.csv','r') #
h=f.readline()
pred['gam']={}
for l in f:
    a=l.rstrip().split(',')
    pred['gam'][str(int(float(a[1])))]=float(a[2])
sds['gam'] = iqr(pred['gam'])
avgs['gam'] = np.median(pred['gam'].values())

f=open('train_gam012.csv','r') #
h=f.readline()
pred['gamt']={}
for l in f:
    a=l.rstrip().split(',')
    pred['gamt'][str(int(float(a[1])))]=float(a[2])
sds['gamt'] = iqr(pred['gamt'])
avgs['gamt'] = np.median(pred['gamt'].values())

f=open('train_gam_ptw.csv','r') #
h=f.readline()
pred['gamtw']={}
for l in f:
    a=l.rstrip().split(',')
    pred['gamtw'][str(int(float(a[1])))]=float(a[2])
sds['gamtw'] = iqr(pred['gamtw'])
avgs['gamtw'] = np.median(pred['gamtw'].values())


f=open('trainrgbmpw_1000_0.05_300_12.csv','r') #
h=f.readline()
pred['rgbmpw']={}
for l in f:
    a=l.rstrip().split(',')
    pred['rgbmpw'][str(int(float(a[1])))]=float(a[2])
sds['rgbmpw'] = iqr(pred['rgbmpw'])
avgs['rgbmpw'] = np.median(pred['rgbmpw'].values())


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
#use = ('xgb','rgbmbw','thg') #3.692892
#use = ('xgb','rgbmbw','rgbmb') #3.694914
#use = ('xgb','rgbmbw','rgbmgxb') #3.696276
#use = ('xgb','rgbmbw','gamt') #3.696720
#use = ('xgb','rgbmbw','rgbmbs') #3.698002
#use = ('xgb','rgbmbw','svm10') #3.700867
use = ('xgb','rgbmbw','rfbw') #3.705123
#use = ('xgb','rgbmbw','rgbmaw') #3.706377
#use = ('xgb','rgbmbw','rgbmg') #3.717443
#use = ('xgb','rgbmbw','gamtw') #3.721757

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
#use = ('xgb','gamtw','svm10','gam') #blstd
#use = ('xgb','gamtw','rgbmbw','rfbw') #3.724878
#use = pred.keys()
#use = ('xgb','gamtw','rgbmbw','rgbmbs','rfbw','svm10','rgbmg','gam') #blstd

#use = ('xgb',) #3.518234
#use = ('xgb','gam') #3.532911
#use = ('xgb','rgbmg') #3.554386
#use = ('xgb','svm10') #3.568073
#use = ('xgb','gamt') #3.570568
#use = ('xgb','rfbw') #3.598991
#use = ('xgb','rgbmb') #3.601399
#use = ('xgb','rgbmaw') #3.613654
#use = ('xgb','rgbmgxb') #3.622075
#use = ('xgb','rgbmbw') #3.619485
#use = ('xgb','rgbmbw','lr1') #3.621898
#use = ('xgb','rgbmbw','gam') #3.619568
#use = ('xgb','rgbmbw','rgbmg') #3.628910
#use = ('xgb','rgbmbw','svm10') #3.629597
#use = ('xgb','rgbmbw','gamt') #3.621651
#use = ('xgb','rgbmbw','rgbmb') #3.622160
#use = ('xgb','rgbmbw','rgbmaw') #3.622825
#use = ('xgb','rgbmbw','rgbmgxb') #3.628665
#use = ('xgb','rgbmbw','rgbmbs') #3.632917
#use = ('xgb','rgbmbw','rfbw') #3.634759
#use = ('xgb','rgbmbw','gamtw') #3.643883
#use = ('xgb','rgbmbw','gamtw','rgbmb') #3.645808
#use = ('xgb','rgbmbw','gamtw','rgbmaw') #3.645875
#use = ('xgb','rgbmbw','gamtw','rgbmg') #3.647454
#use = ('xgb','rgbmbw','gamtw','rgbmgxb') #3.649232
#use = ('xgb','rgbmbw','gamtw','gamt') #3.649463
#use = ('xgb','rgbmbw','gamtw','svm10') #3.652822
#use = ('xgb','rgbmbw','gamtw','rgbmbs') #3.653633
#use = ('xgb','rgbmbw','gamtw','rfbw') #3.654529
#use = ('xgb','rgbmbw','gamtw','rfbw','rfg') #3.654530
#use = ('xgb','rgbmbw','gamtw','rfbw','xgbnw') #3.654543
#use = ('xgb','rgbmbw','gamtw','rfbw','rgbmb') #3.655294
#use = ('xgb','rgbmbw','gamtw','rfbw','rgbmaw') #3.656443
#use = ('xgb','rgbmbw','gamtw','rfbw','rgbmgxb') #3.656872
#use = ('xgb','rgbmbw','gamtw','rfbw','rgbmg') #3.657530
#use = ('xgb','rgbmbw','gamtw','rfbw','svm10') #3.659516
#use = ('xgb','rgbmbw','gamtw','rfbw','rgbmbs') #3.659997
#use = ('xgb','rgbmbw','gamtw','rfbw','svm5') #3.660174
#use = ('xgb','rgbmbw','gamtw','rfbw','svm50') #3.660470
#use = ('xgb','rgbmbw','gamtw','rfbw','gamt') #3.663074
use = ('xgb','rgbmbw','gamtw','rfbw','gamt','svm5') #3.672362
#xgbnw,svm5,rfg

sys.stderr.write( 'sd = {')
for pk in use:
    sys.stderr.write("'%s': %f, " % (pk,sds[pk]))
sys.stderr.write('}\n')
sys.stderr.write( 'avg = {')
for pk in use:
    sys.stderr.write("'%s': %f, " % (pk,avgs[pk]))
sys.stderr.write('}\n')
#sys.exit(0)
for k in pred.keys():
    for i in pred[k].keys():
        pred[k][i] = (pred[k][i] - avgs[k])/sds[k]

sys.stdout.write('y,wt')
for pk in use:
    sys.stdout.write(',%s' % pk)
sys.stdout.write('\n')
#ws={'rfbw': 0.628176, 'svm10': 0.650560, 'gamtw': 0.652506, 'xgb': 3.878341, 'gam': -1.103447, 'rgbmg': -1.282606, 'rgbmbw': 1.562337, 'rgbmbs': -0.090508}

#pp=[]
#pw=[]
#py=[]
for ref in y.keys():
    sys.stdout.write("%s,%s" % (y[ref],wt[ref]))
#    p = 0
    for pk in use:
#        p += ws[pk] * pred[pk][ref]
        sys.stdout.write(',%f' % pred[pk][ref])
#    pp.append(p)
#    py.append(y[ref])
#    pw.append(wt[ref])
    sys.stdout.write('\n')
#sys.stderr.write("AMS %s %s\n" % maxAMS(pp,pw,py))
#ws = { 'xgb':0.582723, 'rgbmg': -0.354122, 'rgbmb': 0.284462, 'svm': 0.218808, 'rgbmbw': 0.350164, 'rfbw': 0.127386, 'gam': -0.209421 }
#print "EventId,LogOdds"
#for ref in y.keys():
#    p = 0
#    for k in pred.keys():
#        if k in ws:
#            p += ws[k]*pred[k][ref]
#    print '%s,%s' % (ref,p*wt[ref])
