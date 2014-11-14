import numpy as np
import sys
import math
import random

alg='rnn'

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
#f=open('predxgb5.csv','r') #3.593036070
#f=open('predxgb_500_300_5_300_2_2_1.csv','r')
#f=open('predxgbs_600_200_5_0_0_1_0_0.05.csv','r')
#f=open('predxgbtr1000.csv','r') #3.6058075
#f=open('predggb_600_6_0.05_1.0_0.0_-1.0_0.0.csv','r')
#f=open('predxgb07_800_100_6_1200_0_2_0_0.05_1.0.csv','r')
#f=open('models/xgb1/predxgb_800_100_6_1200_0_2_0_0.05_1.0.csv','r')
#f=open('models/xgb2/predxgb_800_100_6_1200_0_2_0_0.05_1.0.csv','r')
f=open('models/xgb3/predxgb_800_100_6_1200_0_2_0_0.05_1.0.csv','r')
#f=open('models/xgb1/predxgba_800_100_6_1200_0_2_0_0.05_1.0.csv','r')
pred['xgb']={}
for l in f:
    a=l.rstrip().split(',')
    v=1/(1+math.exp(-float(a[1])))
    pred['xgb'][int(a[0])]=v

#f=open('predcknn.csv','r') #2.4566505928
#f=open('train_cknn_t_bw0.600000_wlr0.000001.csv','r') #
#f=open('train_cknn_t_bw0.600000_wlr0.000010.csv','r')
#f=open('train_cknn_t_bw0.300000_wlr0.000010.csv','r')
#f=open('train_cknn_t_bw1.200000_wlr0.000010.csv','r')
#f=open('train_cknn_t_bw2.400000_wlr0.000010.csv','r')
#f=open('train_cknn_t_bw4.800000_wlr0.000010.csv','r')
#f=open('train_cknn_tf_bw4.800000_wlr0.000010.csv','r')
#f=open('train_cknn_t_bw12.000000_wlr0.000010.csv','r')
#f=open('train_cknn_tlr_bw1.200000_wlr0.000000.csv','r')
#f=open('train_cknn_t_bw0.600000_vs0.070000.csv','r')
f=open('train_cknn_t_bw0.600000_vs0.770000.csv','r')
#f=open('train_cknn_t_bw0.900000_vs0.770000.csv','r')
#f=open('train_cknn_t_bw1.200000_vs0.070000.csv','r')
#f=open('train_cknn_t_bw1.200000_vs0.770000.csv','r')
#f=open('train_cknn_t_bw1.200000_vs0.470000.csv','r')
#f=open('train_cknn_tt_bw1.200000_vs0.770000.csv','r')
#f=open('train_cknn_ts_bw2.400000_vs0.770000.csv','r')
#f=open('train_cknn_ts_bw4.800000_vs0.770000.csv','r')
#f=open('train_cknn_ts_bw9.600000_vs0.770000.csv','r')
#f=open('train_cknn_tc_bw9.600000_vs0.770000.csv','r')
pred['knn']={}
for l in f:
    a=l.rstrip().split(',')
    v=float(a[1])
    pred['knn'][int(a[0])]=v

if alg=='mars':
    #f=open('train_earth.csv','r')
    f=open(sys.argv[1],'r')
    sys.stdout.write('%s ' % sys.argv[1])
    pred['mars']={}
    for l in f:
        a=l.rstrip().split(',')
        v=float(a[1])
        pred['mars'][int(float(a[0]))]=v

f=open('trainrfw_1000_6_10_2.000000.csv','r')
#f=open(sys.argv[1],'r')
#f=open('trainetw_1000_20_10_2.000000.csv','r')
#f=open('trainetw_1000_6_10_2.000000.csv','r')
#f=open('trainrfwx_1000_6_10_2.000000.csv','r')
#f=open('trainrfwsx_1000_6_10_2.000000.csv','r')
pred['rfbw']={}
for l in f:
    a=l.rstrip().split(',')
    v=float(a[1])
    pred['rfbw'][int(float(a[0]))]=v

f=open('models/et1/trainetw_1000_19_10_600_1_2_0.csv','r')
#f=open('models/et2/trainetw_1000_19_10_600_1_2_0.csv','r')
pred['et']={}
for l in f:
    a=l.rstrip().split(',')
    v=float(a[1])
    pred['et'][int(float(a[0]))]=v

#f=open('trainrgbmbw1000_0.05_300_12.csv','r')
#f=open('train_rgbm_1000_300_12_300_2_2_1.csv','r')
#f=open('trainrgbms1000_0.05_300_7.csv','r')
#f=open('train_rgbm_1000_300_3_300_2_2_1.csv','r')
#f=open('trainrgbmbws1000_0.05_300_12_4_4.csv','r')
#f=open('trainrgbmbwsx100_1000_0.05_300_12_2_1.csv','r')
#f=open('trainrgbmbwx_1000_0.05_300_12_2_1.csv','r')
#f=open('trainrgbmb2000_0.05_800_10.csv','r')
#f=open('predbl/train_rgbmbw_1000_0.05_300_12.csv','r')
#f=open('models/rgbmb1/train_rgbmbw_1000_0.05_300_12_600_1_2_0.csv','r')
f=open('models/rgbmb2/train_rgbmbw_1000_0.05_300_12_600_1_2_0.csv','r')
h=f.readline()
pred['rgbmbw']={}
for l in f:
    a=l.rstrip().split(',')
    pred['rgbmbw'][int(float(a[1]))]=float(a[2])

if alg=='rgbmg':
    f=open('trainrgbmg2_1100_0.05_300_7.csv','r')
    h=f.readline()
    pred['rgbmg']={}
    for l in f:
        a=l.rstrip().split(',')
        pred['rgbmg'][int(float(a[1]))]=float(a[2])

f=open('models/rgbma2/train_rgbmaw_1000_0.05_300_12_600_1_2_0.csv','r')
h=f.readline()
pred['rgbma']={}
for l in f:
    a=l.rstrip().split(',')
    pred['rgbma'][int(float(a[1]))]=float(a[2])

#f=open('models/gam1/train_gam_pt.csv','r')
#f=open('models/gam6/train_gam_pw_600_1_2_0.csv','r')
f=open('models/gam2/train_gam_pt.csv','r')
#f=open('train_gam012.csv','r') #
h=f.readline()
pred['gamtw']={}
for l in f:
    a=l.rstrip().split(',')
    pred['gamtw'][int(float(a[1]))]=1/(1+math.exp(-float(a[2])))

if alg=='rnn':
    f=open('train_rnn.csv','r')
    h=f.readline()
    pred['rnn']={}
    for l in f:
        a=l.rstrip().split(',')
        pred['rnn'][int(float(a[1]))]=float(a[2])

if alg=='drgbm':
    f=open('/home/glen/higgs_gbm2.csv','r')
    h=f.readline()
    pred['drgbm']={}
    for l in f:
        a=l.rstrip().split(',')
        pred['drgbm'][int(float(a[0]))]=float(a[1])

if alg=='gamg':
    f=open('models/gamg2/train_gam_pt.csv','r')
    #f=open('train_gam012.csv','r') #
    h=f.readline()
    pred['gamg']={}
    for l in f:
        a=l.rstrip().split(',')
        pred['gamg'][int(float(a[1]))]=float(a[2])

f=open('models/svm1/train_ksvmc10t.csv','r')
#f=open(sys.argv[1],'r')
h=f.readline()
pred['svm10']={}
for l in f:
    a=l.rstrip().split(',')
    pred['svm10'][int(float(a[1]))]=float(a[3])

#f=open('trainstack.csv','r')
#f=open('train_gambl.csv','r')
f=open('test3.out','r')
h=f.readline()
pred['stack']={}
for l in f:
    a=l.rstrip().split(',')
    pred['stack'][int(float(a[0]))]=a[2]=='s'

f=open('training.csv','r')
l=f.readline()
wt={}
y={}
for l in f:
    a=l.rstrip().split(',')
    y[int(a[0])]=(1 if a[32]=='s' else 0)
    wt[int(a[0])]=float(a[31])

#random.seed(1234)
sc=0
for i in y:
    p=min(0.9999,max(0.0001,pred[alg][i]))
    #p=min(0.999,max(0.001,pred['xgb'][i]))
    sc+=y[i]*np.log(p)+(1-y[i])*np.log(1-p)
print -sc/250000

for l in range(1):
    pl=[]
    rc=0
    for i in y.keys():
        #if random.randint(0,100)>60:
        if True:
            pl.append([pred[alg][i],y[i],wt[i]])
            #pl.append([pred['xgb'][i]+pred['knn'][i],y[i],wt[i]])
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
