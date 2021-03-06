from GLM import GLM
import math
import numpy as np
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

pg={}
f=open('predxgb.csv','r') #3.588919
for l in f:
    a=l.rstrip().split(',')
    pg[a[0]]=[float(a[1])]

#f=open('predlr1.csv','r') #3.086161
#f=open('predlr1l.csv','r') #3.219877
#f=open('predlr1lsw.csv','r') #3.231389
#f=open('predlr1lw.csv','r') 
f=open('predlr1lsw2.csv','r') #3.244810
for l in f:
    a=l.rstrip().split(',')
    pg[a[0]].append(1.5+float(a[1]))

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
#f=open('predrgbm_t200_mn500_mf18_lr0p1w4cv3c.csv','r') #3.578656
f=open('predrgbm_t200_mn500_mf18_lr0p1w4cv3ca.csv','r') #3.556618
#f=open('predrgbm_t200_mn500_mf18_lr0p1w4cv3cf18.csv','r') #3.552285
#f=open('predrgbm_t200_mn500_mf18_lr0p1w4cv3clrf.csv','r') #3.519256
#f=open('predrgbm_t200_mn500_mf18_lr0p1w4cv3co.csv','r') #3.491170
h=f.readline()
for l in f:
    #a=l.rstrip().split(',')
    #pg[a[0]].append(1.2+math.log(float(a[1]))-math.log(1-float(a[1])))
    a=l.rstrip().split(',')
    pg[str(int(float(a[1])))].append(2.2+float(a[2]))

#f=open('predrgbmg_t300.csv','r') #2.662905
#f=open('predrgbmgr.csv','r') 
#f=open('predksvm.csv','r') #3.135016
#f=open('predksvmc0p5.csv','r') #3.112735
#f=open('predksvmc5.csv','r') #3.213296
#f=open('predksvmc10.csv','r') #3.199998
#f=open('predrgbmgr.csv','r') 
#f=open('predgam.csv','r') # 3.006094
f=open('predgamsp0.2.csv','r') # 3.041526
h=f.readline()
for l in f:
    a=l.rstrip().split(',')
    pg[str(int(float(a[1])))].append(2.2+float(a[2]))

f=open('training.csv','r')
l=f.readline()
wt={}
jet={}
for l in f:
    a=l.rstrip().split(',')
    pg[a[0]].append(1 if a[32]=='s' else 0)
    wt[a[0]]=float(a[31])
    jet[a[0]]=int(a[23])

#d = np.ascontiguousarray(np.array(pg.values())).astype(float)
#np.savetxt('test.out',d,fmt='%f')
#x = np.ascontiguousarray(np.array(d[:,0:4])).astype(float)
#y = np.ascontiguousarray(np.array(d[:,4])).astype(float)
#m = GLM()
#m.fit(x,y,distribution='Bernoulli')
#print m.coef_
for w2 in(0.0,):
    for w3 in(0,0.05,0.10): #0.05,0.10):
        #for th in (2.82,):
        for th in np.arange(2.0,3.5,0.02):
            s=0
            b=0
            for i,j in pg.items():
                #if m.coef_[0]+m.coef_[1]*j[0]+m.coef_[2]*j[1]+m.coef_[3]*j[2]>th:
                #if (j[0]*(1-w3-w2)+w3*j[1]+w2*j[2])>th:
                #if (j[2]*0.4+0.6*j[0])*j[3]>th:
                if j[3]>th:
                    if j[4]==1:
                        s+=wt[i]
                    else:
                        b+=wt[i]
            print '%f %f %f %f' % (w3,w2,th,AMS(s,b))
