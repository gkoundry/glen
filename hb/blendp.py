from GLM import GLM
import pandas
import random
import copy
import math
import numpy as np
import sys
from itertools import product

def iqr(a):
    return np.percentile(a.values(),90)-np.percentile(a.values(),10)
#sd = {'xgb': 0.951530, 'gamtw': 8.441251, 'rgbmbw': 0.867867, 'rgbmbs': 0.864041, 'rfbw': 0.789340, 'svm10': 0.971562, 'rgbmg': 3.925392, 'gam': 6.049710, }
#avg = {'xgb': 0.420928, 'gamtw': -6.640058, 'rgbmbw': 0.137540, 'rgbmbs': 0.141176, 'rfbw': 0.171310, 'svm10': 0.156137, 'rgbmg': 1.178741, 'gam': -1.224612, }
#sd = {'xgb': 0.951530, 'rgbmbw': 0.867867, }
#avg = {'xgb': 0.420928, 'rgbmbw': 0.137540, }
#sd = {'xgb': 0.951530, 'rgbmbw': 0.867867, 'gamtw': 8.441251, }
#avg = {'xgb': 0.420928, 'rgbmbw': 0.137540, 'gamtw': -6.640058, }
#sd = {'xgb': 0.951530, 'rgbmbw': 0.867867, 'rgbmg': 3.925392, }
#avg = {'xgb': 0.420928, 'rgbmbw': 0.137540, 'rgbmg': 1.178741, }
#sd = {'xgb': 0.951530, 'rgbmbw': 0.867867, 'rgbmaw': 0.880809, }
#avg = {'xgb': 0.420928, 'rgbmbw': 0.137540, 'rgbmaw': 0.133359, }
#sd = {'xgb': 0.951530, 'rgbmbw': 0.867867, 'rfbw': 0.789340, }
#avg = {'xgb': 0.420928, 'rgbmbw': 0.137540, 'rfbw': 0.171310, }
#sd = {'xgb': 0.951530, 'rgbmbw': 0.867867, 'gamtw': 8.441251, 'rfbw': 0.789340, 'gamt': 6.426416, 'svm5': 0.963539, }
#avg = {'xgb': 0.420928, 'rgbmbw': 0.137540, 'gamtw': -6.640058, 'rfbw': 0.171310, 'gamt': -1.280268, 'svm5': 0.153622, }
#sd = {'xgb': 0.951530, 'rgbmbw': 0.867867, 'gamtw': 8.441251, 'rfbw': 0.789340, 'gamt': 6.426416, 'svm10t': 0.852498, }
#avg = {'xgb': 0.420928, 'rgbmbw': 0.137540, 'gamtw': -6.640058, 'rfbw': 0.171310, 'gamt': -1.280268, 'svm10t': 0.829122, }
#sd = {'xgb': 0.951530, 'rgbmbw': 0.867867, 'knnt': 0.347539, }
#avg = {'xgb': 0.420928, 'rgbmbw': 0.137540, 'knnt': 0.388496, }
#sd = {'xgb': 0.951530, 'rgbmaw': 0.880102, 'rfbw': 0.789340, }
#avg = {'xgb': 0.420928, 'rgbmaw': 0.133656, 'rfbw': 0.171310, }
sd = {'xgb': 0.960040, 'rgbmbw': 0.939329, }
avg = {'xgb': 0.398802, 'rgbmbw': 0.306323, }

#ws = {'xgb':0.2725,'rgbmbw':0.5600}
#ws = {'rgbmbw':0.2725,'xgb':0.5600}
ws = {'rgbmbw': 1.643, 'xgb': 1.3044}


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

def psa(k,p):
    if k in sd:
        sys.stderr.write( '%s %s/%s %s/%s\n' % (k,sd[k],iqr(p[k]),avg[k],np.median(p[k].values())))

pred={}
#f=open('predxgbpw.csv','r') #3.588919
f=open('predxgbp_800_100_6_1200_0_2_0_0.05_1.0.csv','r')
pred['xgb']={}
for l in f:
    a=l.rstrip().split(',')
    v=1/(1+math.exp(-float(a[1])))
    pred['xgb'][a[0]]=v
psa('xgb',pred)

#f=open('predlr1.csv','r') #3.086161
#f=open('predlr1l.csv','r') #3.219877
#f=open('predlr1lsw.csv','r') #3.231389
f=open('predlr1lsw2p.csv','r') #3.244810
pred['lr1']={}
for l in f:
    a=l.rstrip().split(',')
    pred['lr1'][a[0]]=float(a[1])
#psa('lr1',pred)

f=open('test.csv','r')
h=f.readline()
idt=[]
for l in f:
    a=l.split(',')
    idt.append(a[0])

f=open('testrgbmb1000_0.05_300_12.csv','r')
h=f.readline()
pred['rgbmb']={}
r=0
for l in f:
    a=l.rstrip().split(',')
    pred['rgbmb'][idt[r]]=float(a[1])
    r+=1
#psa('rgbmb',pred)

f=open('testrgbmbs1000_0.05_300_12.csv','r')
h=f.readline()
pred['rgbmbs']={}
for l in f:
    a=l.rstrip().split(',')
    pred['rgbmbs'][str(int(float(a[1])))]=float(a[2])
psa('rgbmbs',pred)

f=open('testrgbmg1000_0.05_300_12.csv','r')
h=f.readline()
pred['rgbmg']={}
for l in f:
    a=l.rstrip().split(',')
    pred['rgbmg'][str(int(float(a[1])))]=float(a[2])
psa('rgbmg',pred)

#f=open('testrgbmbw1000_0.05_300_12_2_2.csv','r')
f=open('predbl/test_rgbmbw_1000_0.05_300_12.csv','r')
h=f.readline()
pred['rgbmbw']={}
for l in f:
    a=l.rstrip().split(',')
    pred['rgbmbw'][str(int(float(a[1])))]=float(a[2])
psa('rgbmbw',pred)

f=open('testrgbmaw1000_0.05_300_12.csv','r')
h=f.readline()
pred['rgbmaw']={}
for l in f:
    a=l.rstrip().split(',')
    pred['rgbmaw'][str(int(float(a[1])))]=float(a[2])
psa('rgbmaw',pred)

f=open('testrfwx_1000_6_10_2.000000.csv','r') #
#f=open('testrfwt_1000_6_10_2.000000.csv','r') #
pred['rfbw']={}
for l in f:
    a=l.rstrip().split(',')
    pred['rfbw'][str(int(float(a[0])))]=float(a[1])
psa('rfbw',pred)

f=open('test_cknn_t_bw2.400000_wlr0.000010.csv','r')
pred['knnt']={}
for l in f:
    a=l.rstrip().split(',')
    pred['knnt'][str(int(float(a[0])))]=float(a[1])
psa('knnt',pred)

##f=open('predksvm.csv','r') #3.135016
##f=open('predksvmc0p5.csv','r') #3.112735
#f=open('predksvmc5.csv','r') #3.112735
f=open('test_ksvmc5.csv','r')
h=f.readline()
pred['svm5']={}
for l in f:
    a=l.rstrip().split(',')
    pred['svm5'][str(int(float(a[1])))]=float(a[2])
psa('svm5',pred)

f=open('test_ksvmc10t.csv','r')
h=f.readline()
pred['scm10t']={}
for l in f:
    a=l.rstrip().split(',')
    pred['scm10t'][str(int(float(a[1])))]=float(a[3])
psa('scm10t',pred)

f=open('test_ksvmc10.csv','r') #
h=f.readline()
pred['svm10']={}
for l in f:
    a=l.rstrip().split(',')
    pred['svm10'][str(int(float(a[1])))]=float(a[2])
psa('svm10',pred)

f=open('test_ksvmc10t.csv','r') #
h=f.readline()
pred['svm10t']={}
for l in f:
    a=l.rstrip().split(',')
    pred['svm10t'][str(int(float(a[1])))]=float(a[2])
psa('svm10t',pred)

#f=open('predbam.csv','r') #3.135016
f=open('test_gam_v1.csv','r') #
h=f.readline()
pred['gam']={}
for l in f:
    a=l.rstrip().split(',')
    pred['gam'][str(int(float(a[1])))]=float(a[2])
psa('gam',pred)

f=open('test_gam012.csv','r') #
h=f.readline()
pred['gamt']={}
for l in f:
    a=l.rstrip().split(',')
    pred['gamt'][str(int(float(a[1])))]=float(a[2])
psa('gamt',pred)

f=open('test_gam_ptw.csv','r') #
h=f.readline()
pred['gamtw']={}
for l in f:
    a=l.rstrip().split(',')
    pred['gamtw'][str(int(float(a[1])))]=float(a[2])
psa('gamtw',pred)

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
#bl7
#ws = {'xgb': 1.808217, 'rgbmg': -1.369249, 'rgbmb': 1.623148, 'svm':  0.465914, 'rgbmbw': 0.328718, 'rfbw': 0.428909, 'gam': -0.548600 }
#bl6
#ws = {'xgb': 1.547173, 'rgbmg': -1.039914, 'rgbmb': 1.275528, 'rgbmbw': 0.467442, 'rfbw': 0.403140, 'gam': -0.403513 }
#ns
#ws = { 'xgb':0.582723, 'rgbmg': -0.354122, 'rgbmb': 0.284462, 'svm': 0.218808, 'rgbmbw': 0.350164, 'rfbw': 0.127386, 'gam': -0.209421 }
#y,wt,xgb,gamtw,rgbmbw,rgbmbs,rfbw,svm10,rgbmg,gam
#ws = { 'xgb': 1.112781, 'gamtw': -0.055742, 'rgbmbw': 0.222131, 'rgbmbs': 0.043973, 'rfbw': 0.214647, 'svm10':  0.115873, 'rgbmg': -0.068166, 'gam': -0.173238 }
#ws={ 'xgb': 5.397434, 'gamtw': 2.280759, 'rgbmbw': 2.574913, 'rgbmbs': 0.195464, 'rfbw': 1.306721, 'svm10': 0.589743, 'rgbmg': -0.465206, 'gam': -2.068766 }
#ws={'rfbw': 0.628176, 'svm10': 0.650560, 'gamtw': 0.652506, 'xgb': 3.878341, 'gam': -1.103447, 'rgbmg': -1.282606, 'rgbmbw': 1.562337, 'rgbmbs': -0.090508}
#ws={'rfbw': 0.180953, 'svm10': 0.868917, 'gamtw': 3.058251, 'xgb': 1.988539, 'gam': -1.238492, 'rgbmg': -0.627742, 'rgbmbw': 0.083814, 'rgbmbs': 1.237639}
#ws={'rgbmbw': 0.276681, 'xgb': 1.00209}
#ws={'rgbmbw': 0.246103, 'xgb': 0.711738, 'gamtw': 0.436929}
#ws={'rgbmg': -0.593754, 'rgbmbw': 0.553037, 'xgb': 2.170524}
#ws={'rgbmbw': 1.037678, 'xgb': 4.858884, 'rfbw': 0.321358}
#ws={'gamt': -1.202937, 'rfbw': 0.637227, 'gamtw': 2.434136, 'xgb': 2.021024, 'svm5': 0.403495, 'rgbmbw': 1.004861} #predblavg
#ws={'gamt': -0.72845, 'rfbw': 0.460331, 'gamtw': 1.710972, 'xgb': 0.420878, 'svm5': 0.23327, 'rgbmbw': 0.736339} #sqrt
#ws={'gamt': 0.031443, 'rfbw': 0.405169, 'gamtw': 0.40533, 'xgb': 1.339638, 'svm5': 0.313695, 'rgbmbw': 0.427382} #sqrt2
#ws={'gamt': -0.496129, 'rfbw': 0.210772, 'gamtw': 0.962522, 'xgb': 0.661007, 'rgbmbw': 0.382076, 'svm10t': -0.244178} #svm10t
#ws={'rgbmbw': 0.160479, 'xgb': 1.072316, 'knnt': 1.010216}
#ws={'rgbmaw': 1.698562, 'xgb': 3.926927, 'rfbw': 0.926702}
#ws={'rfbw': 0.20248, 'gamtw': 0.904874, 'xgb': 1.409318, 'rgbmbw': 0.810666, 'knnt': 0.055273, 'svm10t': -0.265887}
#ws={'rgbmbw': 0.75,'xgb':0.25}
th=0.760000

#for k in ws.keys():
#    for i in pred[k].keys():
#        pred[k][i] = (pred[k][i] - avg[k])/sd[k]
pl=[]
for i,a in pred['xgb'].items():
    p = 0
    for k in ws.keys():
        p += ws[k]*pred[k][i]
    pl.append((i,p))

print 'EventId,RankOrder,Class'
r=1
pos=0
for i in sorted(pl,key=lambda x:-x[1]):
    print '%s,%s,%s' % (i[0],r,'s' if i[1]>th else 'b')
    #print '%s,%s' % (i[0],i[1])
    if i[1]>th:
        pos+=1
    r+=1
sys.stderr.write('pos %f\n' % (pos/550000.0))
