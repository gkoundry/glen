from GLM import GLM
import math
import numpy as np

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

f=open('predlr1.csv','r')
for l in f:
    a=l.rstrip().split(',')
    pg[a[0]].append(float(a[1]))

#f=open('predrgbm_200_0.100000.csv','r') #3.454425
#f=open('predrgbm_400.csv','r') #3.403357
f=open('predrgbm_300_0.100000_200.csv','r') #3.480559
for l in f:
    a=l.rstrip().split(',')
    pg[a[0]].append(1.2+math.log(float(a[1]))-math.log(1-float(a[1])))

f=open('training.csv','r')
l=f.readline()
wt={}
for l in f:
    a=l.rstrip().split(',')
    pg[a[0]].append(1 if a[32]=='s' else 0)
    wt[a[0]]=float(a[31])

d = np.ascontiguousarray(np.array(pg.values())).astype(float)
np.savetxt('test.out',d,fmt='%f')
x = np.ascontiguousarray(np.array(d[:,0:3])).astype(float)
y = np.ascontiguousarray(np.array(d[:,3])).astype(float)
m = GLM()
m.fit(x,y,distribution='Bernoulli')
print m.coef_
for w1 in(0,): #0.05,):
    for w2 in(1,): #0.15,0.2,0.25,0.3):
        for th in np.arange(2.1,3.1,0.02):
            s=0
            b=0
            for i,j in pg.items():
                #if m.coef_[0]+m.coef_[1]*j[0]+m.coef_[2]*j[1]+m.coef_[3]*j[2]>th:
                #if (j[0]*(1-w1-w2)+w1*j[1]+w2*j[2])>th:
                if j[2]>th:
                    if j[3]==1:
                        s+=wt[i]
                    else:
                        b+=wt[i]
            print '%f %f %f %f' % (w1,w2,th,AMS(s,b))
