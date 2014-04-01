import cPickle
from collections import defaultdict
pred=cPickle.load(open('pred.pkl','rb'))
f=open('trains3.csv','r')
h=f.readline()
ic=0
ic1=0
c=0
t=0
c1=0
t1=0
sm=0
mt=0
icd=defaultdict(int)
icd1=defaultdict(int)
for l in f:
    a=l.rstrip().split(',')
    if a[2]=='1':
        id = int(a[0])
        p = []
        pl = []
        for i in ('A','B','C','D','E','F','G'):
            pl.append(lasta[ord(i)-65+17])
            if id in pred[i]:
                p.append(str(int(pred[i][id])))
            else:
                p.append(lasta[ord(i)-65+17])
            if p[-1]==a[ord(i)-65+17] and id in pred[i]:
                mt += 1
            if p[-1]==a[ord(i)-65+17]:
                ic += 1
                icd[i] += 1
            if pl[-1]==a[ord(i)-65+17]:
                ic1 += 1
                icd1[i] += 1
        if p!=pl:
            print '%s %s %s %d %d' % (a[17:24],pl,p,a[17:24]==pl,a[17:24]==p)
        if a[17:24]==p:
            c+=1
        if a[17:24]==pl:
            c1+=1
        if p==pl:
            sm+=1
        #print str(a[17:24])
        #print ' '+str(pl)
        #print ' '+str(p)
        t+=1
    lasta=a
print c*1.0/t
print c1*1.0/t
print str(c1)+' '+str(t)
print sm
print ic*1.0/(7*t)
print ic1*1.0/(7*t)
print mt
for i in ('A','B','C','D','E','F','G'):
    print i+' '+str(icd[i])+' '+str(icd1[i])+' '+str(icd[i]-icd1[i])
