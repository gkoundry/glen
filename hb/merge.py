import pandas
import random
import copy
import math
import numpy as np
import sys
from itertools import product

use = ('rgbmbw','xgb2')

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

if 'xgg' in use:
    f=open('predggb_600_6_0.05_5.0_1.0_-1.0_0.0.csv','r')
    #f=open('predxgg5.csv','r') #3.588919
    pred['xgg']={}
    for l in f:
        a=l.rstrip().split(',')
        v=1/(1+math.exp(-float(a[1])))
        pred['xgg'][a[0]]=v
    sds['xgg'] = iqr(pred['xgg'])
    avgs['xgg'] = np.median(pred['xgg'].values())

if 'xgb' in use:
    f=open('predxgb_500_300_5_300_2_2_1.csv','r') #3.588919
    #f=open('predxgb5.csv','r') #3.588919
    pred['xgb']={}
    for l in f:
        a=l.rstrip().split(',')
        v=1/(1+math.exp(-float(a[1])))
        pred['xgb'][a[0]]=v
    sds['xgb'] = iqr(pred['xgb'])
    avgs['xgb'] = np.median(pred['xgb'].values())

if 'xgb2' in use:
    #f=open('predxgb_500_300_5_300_2_2_1.csv','r') #3.588919
    f=open('predxgb07_800_100_6_1200_0_2_0_0.05_1.0.csv','r')
    pred['xgb2']={}
    for l in f:
        a=l.rstrip().split(',')
        v=1/(1+math.exp(-float(a[1])))
        pred['xgb2'][a[0]]=v
    sds['xgb2'] = iqr(pred['xgb2'])
    avgs['xgb2'] = np.median(pred['xgb2'].values())

if 'knn' in use:
    f=open('predcknn.csv','r') #
    pred['knn']={}
    for l in f:
        a=l.rstrip().split(',')
        v=float(a[1])
        pred['knn'][a[0]]=v
    sds['knn'] = iqr(pred['knn'])
    avgs['knn'] = np.median(pred['knn'].values())

if 'knnt' in use:
    #f=open('train_cknn_t_bw0.600000_wlr0.000001.csv','r') #
    #f=open('train_cknn_t_bw0.600000_wlr0.000010.csv','r')
    #f=open('train_cknn_t_bw1.200000_wlr0.000010.csv','r')
    #f=open('train_cknn_t_bw2.400000_wlr0.000010.csv','r')
    #f=open('train_cknn_t_bw4.800000_wlr0.000010.csv','r')
    #f=open('train_cknn_t_bw0.600000_vs0.770000.csv','r')
    #f=open('train_cknn_t_bw1.200000_vs0.770000.csv','r')
    f=open('train_cknn_ts_bw4.800000_vs0.770000.csv','r')
    pred['knnt']={}
    for l in f:
        a=l.rstrip().split(',')
        v=float(a[1])
        pred['knnt'][a[0]]=v
    sds['knnt'] = iqr(pred['knnt'])
    avgs['knnt'] = np.median(pred['knnt'].values())

if 'thg' in use:
    f=open('trainthg.csv','r') #
    pred['thg']={}
    for l in f:
        a=l.rstrip().split(',')
        pred['thg'][a[0]]=float(a[1])
    sds['thg'] = iqr(pred['thg'])
    avgs['thg'] = np.median(pred['thg'].values())

if 'xgbnw' in use:
    f=open('predxgbtr1000nw.csv','r')
    pred['xgbnw']={}
    for l in f:
        a=l.rstrip().split(',')
        pred['xgbnw'][a[0]]=float(a[1])
    sds['xgbnw'] = iqr(pred['xgbnw'])
    avgs['xgbnw'] = np.median(pred['xgbnw'].values())

if 'lr1' in use:
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

if 'rgbmb' in use:
    f=open('trainrgbmb1000_0.05_300_12.csv','r')
    #f=open('trainrgbmb2000_0.05_300_12.csv','r')
    h=f.readline()
    pred['rgbmb']={}
    for l in f:
        a=l.rstrip().split(',')
        pred['rgbmb'][str(int(float(a[1])))]=float(a[2])
    sds['rgbmb'] = iqr(pred['rgbmb'])
    avgs['rgbmb'] = np.median(pred['rgbmb'].values())

if 'rgbmbs' in use:
    f=open('trainrgbmbs1000_0.05_300_12.csv','r')
    h=f.readline()
    pred['rgbmbs']={}
    for l in f:
        a=l.rstrip().split(',')
        pred['rgbmbs'][str(int(float(a[1])))]=float(a[2])
    sds['rgbmbs'] = iqr(pred['rgbmbs'])
    avgs['rgbmbs'] = np.median(pred['rgbmbs'].values())

if 'gamt' in use:
    f=open('train_gam012.csv','r') #
    h=f.readline()
    pred['gamt']={}
    for l in f:
        a=l.rstrip().split(',')
        pred['gamt'][str(int(float(a[1])))]=float(a[2])
    sds['gamt'] = iqr(pred['gamt'])
    avgs['gamt'] = np.median(pred['gamt'].values())

if 'rgbmgp' in use:
    f=open('train_rgbmgp_1000_0.05_300_12.csv','r')
    h=f.readline()
    pred['rgbmgp']={}
    for l in f:
        a=l.rstrip().split(',')
        v=math.exp(float(a[2]))
        pred['rgbmgp'][str(int(float(a[1])))]=v
    sds['rgbmgp'] = iqr(pred['rgbmgp'])
    avgs['rgbmgp'] = np.median(pred['rgbmgp'].values())

if len(set(('rgbmgxb','rgbmg','rgbmg2','rgbmgxx','rgbmgxg')) & set(use)):
    #f=open('train_rgbmgp_1000_0.05_300_12.csv','r')
    f=open('trainrgbmg_1000_0.05_300_12.csv','r')
    #f=open('trainrgbmg_-0.5_1000_0.05_300_12.csv','r') #3.298684
    #f=open('trainrgbmg_-1_1000_0.05_300_12.csv','r') #
    h=f.readline()
    pred['rgbmg']={}
    pred['rgbmg2']={}
    #pred['rgbmgxb']={}
    #pred['rgbmgxx']={}
    #pred['rgbmgxg']={}
    for l in f:
        a=l.rstrip().split(',')
        #v=math.exp(float(a[2]))
        v=float(a[2])
        pred['rgbmg'][str(int(float(a[1])))]=v
        pred['rgbmg2'][str(int(float(a[1])))]=float(a[2])*float(a[2])
        #pred['rgbmgxb'][str(int(float(a[1])))]=(10-pred['rgbmg'][str(int(float(a[1])))])*pred['rgbmb'][str(int(float(a[1])))]
        #pred['rgbmgxx'][str(int(float(a[1])))]=(10-pred['rgbmg'][str(int(float(a[1])))])*pred['xgbnw'][str(int(float(a[1])))]
        #pred['rgbmgxg'][str(int(float(a[1])))]=(10-pred['rgbmg'][str(int(float(a[1])))])*pred['gamt'][str(int(float(a[1])))]
    sds['rgbmg'] = iqr(pred['rgbmg'])
    avgs['rgbmg'] = np.median(pred['rgbmg'].values())
    sds['rgbmg2'] = iqr(pred['rgbmg2'])
    avgs['rgbmg2'] = np.median(pred['rgbmg2'].values())
    #sds['rgbmgxb'] = iqr(pred['rgbmgxb'])
    #avgs['rgbmgxb'] = np.median(pred['rgbmgxb'].values())
    #sds['rgbmgxx'] = iqr(pred['rgbmgxx'])
    #avgs['rgbmgxx'] = np.median(pred['rgbmgxx'].values())
    #sds['rgbmgxg'] = iqr(pred['rgbmgxg'])
    #avgs['rgbmgxg'] = np.median(pred['rgbmgxg'].values())

if 'rgbmbw2' in use:
    f=open('train_rgbmbw_1000_0.05_300_12_1200_2.csv','r')
    h=f.readline()
    pred['rgbmbw2']={}
    for l in f:
        a=l.rstrip().split(',')
        pred['rgbmbw2'][str(int(float(a[1])))]=float(a[2])
    sds['rgbmbw2'] = iqr(pred['rgbmbw2'])
    avgs['rgbmbw2'] = np.median(pred['rgbmbw2'].values())

if 'rgbmbw' in use:
    #f=open('trainrgbmbw1000_0.05_300_12.csv','r')
    #f=open('trainrgbmbws1000_0.05_300_12.csv','r')
    #f=open('trainrgbmbwsx100_1000_0.05_300_12_2_1.csv','r')
    f=open('predbl/train_rgbmbw_1000_0.05_300_12.csv','r')
    #f=open('train_rgbmbw_1000_0.05_300_12_1200_2.csv','r')
    h=f.readline()
    pred['rgbmbw']={}
    for l in f:
        a=l.rstrip().split(',')
        pred['rgbmbw'][str(int(float(a[1])))]=float(a[2])
    sds['rgbmbw'] = iqr(pred['rgbmbw'])
    avgs['rgbmbw'] = np.median(pred['rgbmbw'].values())

if 'tbb' in 'use':
    f=open('traintbb_200_5_500.csv','r') #
    pred['tbb']={}
    for l in f:
        a=l.rstrip().split(',')
        pred['tbb'][str(int(float(a[0])))]=float(a[1])
    sds['tbb'] = iqr(pred['tbb'])
    avgs['tbb'] = np.median(pred['tbb'].values())

if 'rfbw' in use:
    f=open('prednw/trainrfw_1000_6_10_2.000000.csv','r')
    #f=open('trainrfw_1000_6_10_2.000000.csv','r') #
    #f=open('trainrf_200_10_5.csv','r')
    #f=open('trainrfwt_1000_6_10_2.000000.csv','r') #
    pred['rfbw']={}
    for l in f:
        a=l.rstrip().split(',')
        pred['rfbw'][str(int(float(a[0])))]=float(a[1])
    sds['rfbw'] = iqr(pred['rfbw'])
    avgs['rfbw'] = np.median(pred['rfbw'].values())

if 'rfg' in use:
    f=open('trainrfg_500_16_10.csv','r') #
    pred['rfg']={}
    for l in f:
        a=l.rstrip().split(',')
        pred['rfg'][str(int(float(a[0])))]=float(a[1])
    sds['rfg'] = iqr(pred['rfg'])
    avgs['rfg'] = np.median(pred['rfg'].values())

if 'rgbmaw' in use:
    f=open('trainrgbmaw1000_0.05_300_12.csv','r')
    h=f.readline()
    pred['rgbmaw']={}
    for l in f:
        a=l.rstrip().split(',')
        pred['rgbmaw'][str(int(float(a[1])))]=float(a[2])
    sds['rgbmaw'] = iqr(pred['rgbmaw'])
    avgs['rgbmaw'] = np.median(pred['rgbmaw'].values())

if 'svm50' in use:
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

if 'svm10' in use:
    f=open('train_ksvmc10.csv','r') #
    h=f.readline()
    pred['svm10']={}
    for l in f:
        a=l.rstrip().split(',')
        pred['svm10'][str(int(float(a[1])))]=float(a[2])
    sds['svm10'] = iqr(pred['svm10'])
    avgs['svm10'] = np.median(pred['svm10'].values())

if 'svm10t' in use:
    f=open('train_ksvmc10t.csv','r') #
    h=f.readline()
    pred['svm10t']={}
    for l in f:
        a=l.rstrip().split(',')
        pred['svm10t'][str(int(float(a[1])))]=float(a[2])
    sds['svm10t'] = iqr(pred['svm10t'])
    avgs['svm10t'] = np.median(pred['svm10t'].values())

if 'svm5' in use:
    f=open('train_ksvmc5.csv','r')
    h=f.readline()
    pred['svm5']={}
    for l in f:
        a=l.rstrip().split(',')
        pred['svm5'][str(int(float(a[1])))]=float(a[2])
    sds['svm5'] = iqr(pred['svm5'])
    avgs['svm5'] = np.median(pred['svm5'].values())

if 'gam' in use:
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

if 'gamtw' in use:
    f=open('train_gam_ptw.csv','r') #
    h=f.readline()
    pred['gamtw']={}
    for l in f:
        a=l.rstrip().split(',')
        pred['gamtw'][str(int(float(a[1])))]=1/(1+math.exp(-float(a[2])))
    sds['gamtw'] = iqr(pred['gamtw'])
    avgs['gamtw'] = np.median(pred['gamtw'].values())

if 'rgbmpw' in use:
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

sys.stderr.write( 'sd = {')
for pk in use:
    sys.stderr.write("'%s': %f, " % (pk,sds[pk]))
sys.stderr.write('}\n')
sys.stderr.write( 'avg = {')
for pk in use:
    sys.stderr.write("'%s': %f, " % (pk,avgs[pk]))
sys.stderr.write('}\n')
#for k in pred.keys():
#    for i in pred[k].keys():
#        pred[k][i] = (pred[k][i] - avgs[k])/sds[k]

out=open('merge1.csv','w')
out.write('id,y,sc')
for pk in use:
    out.write(',%s' % pk)
out.write('\n')
#ws={'rfbw': 0.628176, 'svm10': 0.650560, 'gamtw': 0.652506, 'xgb': 3.878341, 'gam': -1.103447, 'rgbmg': -1.282606, 'rgbmbw': 1.562337, 'rgbmbs': -0.090508}

#pp=[]
#pw=[]
#py=[]
for ref in y.keys():
    out.write("%s,%s,%s" % (ref,y[ref],wt[ref]))
#    p = 0
    for pk in use:
#        p += ws[pk] * pred[pk][ref]
        out.write(',%f' % pred[pk][ref])
#    pp.append(p)
#    py.append(y[ref])
#    pw.append(wt[ref])
    out.write('\n')
out.close()
##sys.stderr.write("AMS %s %s\n" % maxAMS(pp,pw,py))
##ws = { 'xgb':0.582723, 'rgbmg': -0.354122, 'rgbmb': 0.284462, 'svm': 0.218808, 'rgbmbw': 0.350164, 'rfbw': 0.127386, 'gam': -0.209421 }
#ws={'gamt': -1.202937, 'rfbw': 0.637227, 'gamtw': 2.434136, 'xgb': 2.021024, 'svm5': 0.403495, 'rgbmbw': 1.004861}
#print "EventId,Pred"
#for ref in y.keys():
#    p = 0
#    for k in pred.keys():
#        if k in ws:
#            p += ws[k]*pred[k][ref]
#    print '%s,%s' % (ref,1/(1+math.exp(-p)))
