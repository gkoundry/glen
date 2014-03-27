import sys
from collections import defaultdict
#f=open('prior2.txt','r')
#pr = {}
#for l in f:
#    a=l.rstrip().split()
#    pr[a[0]] = a[8]
pr = defaultdict(int)
f=open('train.csv','r')
for l in f:
    a=l.rstrip().split(',')
    id=a[0]
    rt=a[2]
    if rt=='1':
        pr[''.join(a[17:24])]+=1

f=open('trains.csv','r')
h=f.readline()
bc=defaultdict(int)
fc=defaultdict(int)
lc=defaultdict(int)
nc=defaultdict(int)
freq={}
for v in (17,18,19,20,21,22,23):
    freq[v]=defaultdict(int)
pc = 0
lpc = 0
tot = 0
seen = []
for l in f:
    a=l.rstrip().split(',')
    id=a[0]
    rt=a[2]
    if rt=='1':
        predl = ''
        predf = ''
        for v in (17,18,19,20,21,22,23):
            best=0
            mf=[]
            for k,l in freq[v].items():
                if l > best:
                    best=l
                    mf=[]
                if l == best:
                    mf.append(k)
            predl += last[v]
            if last[v] in mf:
                predf += last[v]
            else:
                predf += mf[-1]
            if a[v] in mf:
                if last[v] == a[v]:
                    bc[v]+=1
                else:
                    fc[v]+=1
            else:
                if last[v] == a[v]:
                    lc[v]+=1
                else:
                    nc[v]+=1
            freq[v]=defaultdict(int)
        if predl==''.join(a[17:24]):
            lpc+=1
        if (pr.get(predf,99999)+100) / (pr.get(predl,99998)+100)>2 and predf in seen:
            if predf==''.join(a[17:24]):
                pc+=1
            print a[0]+' '+''.join(a[17:24])+' '+predl+' '+predf+' f '+str(pc)+' '+str(predf==''.join(a[17:24]))+' '+str(predf==predl)
        else:
            if predl==''.join(a[17:24]):
                pc+=1
            print a[0]+' '+''.join(a[17:24])+' '+predl+' '+predf+' l '+str(pc)
        tot +=1
        seen=[]
    else:
        seen.append(''.join(a[17:24]))
        for v in (17,18,19,20,21,22,23):
            freq[v][a[v]]+=1
    last = a
print pc*1.0/tot
print lpc*1.0/tot
for v in (17,18,19,20,21,22,23):
    a= (bc[v]+fc[v]+lc[v]+nc[v])
    print '%d bc %d (%.2f) fc %d (%.3f) lc %d (%.3f) nc %d' % (v-16,bc[v],(bc[v]*1.0/a),fc[v],fc[v]*1.0/a,lc[v],lc[v]*1.0/a,nc[v])
