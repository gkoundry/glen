import numpy as np
import math
import sys

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

files=[
    'train_rgbmv1.csv',
#    'lrgbm.csv',
#    'predbam.csv',
#    'predgam.csv',
#    'predgamsp0.2.csv',
#    'predksvmc0p5.csv',
#    'predksvmc10.csv',
#    'predksvmc5.csv',
#    'predksvm.csv',
#    'predlr1.csv',
#    'predlr1l.csv',
    'predlr1lsw2.csv',
#    'predlr1lsw.csv',
#    'predlr1lw.csv',
#    'predrgbm_500_0.100000_200.csv',
#    'predrgbm.csv',
#    'predrgbmg.csv',
#    'predrgbmgr.csv',
#    'predrgbmg_t300.csv',
#    'predrgbm_t10_mn500_mf11_lr0p1w4cv3c.csv',
#    'predrgbm_t200_mn500_mf11_lr0p1w4cv3c.csv',
#    'predrgbm_t200_mn500_mf18_lr0p1w4cv3ca.csv',
#    'predrgbm_t200_mn500_mf18_lr0p1w4cv3cf18.csv',
#    'predrgbm_t200_mn500_mf18_lr0p1w4cv3clrf.csv',
#    'predrgbm_t200_mn500_mf18_lr0p1w4cv3co.csv',
#    'predrgbm_t300_mn500_mf7_lr0p1.csv',
#    'predrgbm_t300_mn500_mf7_lr0p1w2.csv',
#    'predrgbm_t300_mn500_mf7_lr0p1w4.csv',
#    'predrgbm_t300_mn500_mf7_lr0p1w4cv5c.csv',
#    'predrgbm_t300_mn500_mf7_lr0p1w4cv5.csv',
#    'predrgbm_t300_mn500_mf7_lr0p1w6.csv',
#    'predrgbm_t200_mn500_mf18_lr0p1w4cv3ct123.csv',
    'predxgb.csv']
f=open('training.csv','r')
l=f.readline()
wt={}
y={}
for l in f:
    a=l.rstrip().split(',')
    y[int(a[0])]=(1 if a[32]=='s' else 0)
    wt[int(a[0])]=float(a[31])

pred={}
for fn in files:
    #sys.stdout.write( fn )
    f=open(fn,'r')
    pred[fn]={}
    for l in f:
        a=l.rstrip().split(',')
        try:
            i = int(float(a[-2]))
        except:
            continue
        v=float(a[-1])
        pred[fn][i] = v
#    bestsc=0
#    bestth=0
#    v = sorted(pred[fn].values())
#    mn=v[20000]
#    mx=v[240000]
#    for th in np.arange(mn,mx,0.02):
#        sc=0
#        bc=0
#        for i,j in pred[fn].items():
#            if j>th:
#                if y[i]==1:
#                    sc+=wt[i]
#                else:
#                    bc+=wt[i]
#        sc=AMS(sc,bc)
#        if sc>bestsc:
#            bestsc=sc
#            bestth=th
#        #sys.stdout.write(' %f %f\n' % (th,sc))
#    sys.stdout.write(' %f %f\n' % (bestth,bestsc))
#    sys.stdout.flush()
#    #print len(pred[fn].keys())
th={}
th['train_rgbmv1.csv']=1.302835 #3.592196
#th['lrgbm.csv']=1.045483 #3.245346
#th['predbam.csv']=1.138408 #3.054301
#th['predgam.csv']=0.982657 #3.007818
#th['predgamsp0.2.csv']=1.042350 #3.040580
#th['predksvmc0p5.csv']=0.759561 #3.113347
#th['predksvmc10.csv']=0.772996 #3.195504
#th['predksvmc5.csv']=0.752903 #3.215783
#th['predksvm.csv']=0.738391 #3.157643
#th['predlr1.csv']=1.062900 #3.082239
#th['predlr1l.csv']=0.973159 #3.218471
th['predlr1lsw2.csv']=1.045483 #3.245346
#th['predlr1lsw.csv']=1.134640 #3.230678
#th['predlr1lw.csv']=0.977601 #3.193640
#th['predrgbm_500_0.100000_200.csv']=0.835433 #3.499930
#th['predrgbm.csv']=1.413354 #3.479690
#th['predrgbmg.csv']=-0.400616 #2.663834
#th['predrgbmgr.csv']=0.101220 #1.000771
#th['predrgbmg_t300.csv']=-0.442652 #2.664312
#th['predrgbm_t10_mn500_mf11_lr0p1w4cv3c.csv']=0.210366 #2.860677
#th['predrgbm_t200_mn500_mf11_lr0p1w4cv3c.csv']=1.277847 #3.568547
#th['predrgbm_t200_mn500_mf18_lr0p1w4cv3ca.csv']=0.576450 #3.558090
#th['predrgbm_t200_mn500_mf18_lr0p1w4cv3cf18.csv']=1.206736 #3.548510
#th['predrgbm_t200_mn500_mf18_lr0p1w4cv3clrf.csv']=1.054012 #3.520055
#th['predrgbm_t200_mn500_mf18_lr0p1w4cv3co.csv']=1.002423 #3.491657
#th['predrgbm_t300_mn500_mf7_lr0p1.csv']=1.363293 #3.515896
#th['predrgbm_t300_mn500_mf7_lr0p1w2.csv']=0.788955 #3.526037
#th['predrgbm_t300_mn500_mf7_lr0p1w4.csv']=1.323005 #3.548952
#th['predrgbm_t300_mn500_mf7_lr0p1w4cv5c.csv']=1.203771 #3.563571
#th['predrgbm_t300_mn500_mf7_lr0p1w4cv5.csv']=1.130336 #3.560073
#th['predrgbm_t300_mn500_mf7_lr0p1w6.csv']=1.441803 #3.537564
#th['predrgbm_t200_mn500_mf18_lr0p1w4cv3ct123.csv']=1.199218 #3.478846
th['predxgb.csv']=2.808561 #3.581830
for fn in th.keys():
    sys.stdout.write("%s," % fn)
sys.stdout.write('y,wt\n')
sc=0
bc=0
for i in y.keys():
    oth = 0
    cnt = 0
    for fn in th.keys():
        p = pred[fn][i]>th[fn]
        sys.stdout.write("%d," % p)
        if fn!='predxgb.csv':
            oth+=p
            cnt+=1
    if oth*1.0/cnt>0.55:
        if y[i]==1:
            sc+=wt[i]
        else:
            bc+=wt[i]
    sys.stdout.write("%d,%f\n" % (y[i],wt[i]))
#print AMS(sc,bc)
