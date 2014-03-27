import sys
from collections import defaultdict
f=open('trainrs.csv','r')
h=f.readline()
count={}
quotes={}
levels = { 'A':set(),'B':set(),'C':set(),'D':set(),'E':set(),'F':set(),'G':set() }
last={}
y={}
lmax=0
freq={}
hf=defaultdict(int)
mf={}
age={}
mfage={}
for v in (17,18,19,20,21,22,23):
    freq[v]=defaultdict(int)
for l in f:
    a=l.rstrip().split(',')
    id=a[0]
    if id not in mf:
        mf[id]={}
    rt=a[2]
    if id not in count:
        count[id]= defaultdict(int)
        quotes[id] = 0
        last[id] = {}
        mfage[id] = {}
    if rt=='1':
        y[id]={}
        for v in (17,18,19,20,21,22,23):
            hf = defaultdict(int)
            freq[v]=defaultdict(int)
            y[id][chr(v+48)] = a[v]
            mfage[id][chr(v+48)]=age[v]
    else:
        quotes[id] += 1
        lasta = a
        for v in (17,18,19,20,21,22,23):
            levels[chr(v+48)].add(a[v])
            count[id][chr(v+48)+a[v]] += 1
            last[id][chr(v+48)] = a[v]
            freq[v][a[v]]+=1
#            if id=='10000000':
#                print '%d %s %d %d' % (v,a[v],freq[v][a[v]],hf[v])
            if freq[v][a[v]] > hf[v]:
                hf[v] = freq[v][a[v]]
                mf[id][chr(v+48)]=[]
            if freq[v][a[v]] >= hf[v]:
                mf[id][chr(v+48)].append(a[v])
                age[v]=0
            age[v]+=1

f = open ('train3.csv','w')
f.write('id,y,last,mf,quotes,mfc,mfp,lsc,lsp,mfage,lspr,mfpr,A,B,C,D,E,F,G\n')
for yl in ('A','B','C','D','E','F','G'):
    #f = open ('train3'+yl+'.csv','w')
    #f.write('id,y,last,mf,quotes,mfc,mfp,lsc,lsp,mfage,lspr,mfpr')
    #for yl2 in ('A','B','C','D','E','F','G'):
    #    for l in range(len(levels[yl2])):
    #        f.write(',%s_last_%d' % (yl2,l))
    #    for l in range(len(levels[yl2])):
    #        f.write(',%s_mf_%d' % (yl2,l))
    #f.write('\n')
    freq=defaultdict(int)
    for id in y.keys():
        mf1 = mf[id][yl][-1]
        ls1 = last[id][yl]
        ans = y[id][yl]
        if mf1==ls1 or ans not in (mf1,ls1):
            freq[ans]+=1

    for id in y.keys():
        mf1 = mf[id][yl][-1]
        ls1 = last[id][yl]
        ans = y[id][yl]
        if mf1==ls1 or ans not in (mf1,ls1):
            continue
        f.write(id+','+str(int((ls1==ans)))+','+ls1+','+mf1+','+str(quotes[id]))
        f.write(',%d,%f,%d,%f,%d,%d,%d' % (count[id][yl+mf1],count[id][yl+mf1]*1.0/quotes[id],count[id][yl+ls1],count[id][yl+ls1]*1.0/quotes[id],mfage[id][yl],freq[ls1],freq[mf1]))
        f.write(",%d" % int(yl=='A'))
        f.write(",%d" % int(yl=='B'))
        f.write(",%d" % int(yl=='C'))
        f.write(",%d" % int(yl=='D'))
        f.write(",%d" % int(yl=='E'))
        f.write(",%d" % int(yl=='F'))
        f.write(",%d" % int(yl=='G'))
        #for yl2 in ('A','B','C','D','E','F','G'):
        #    for l in range(len(levels[yl2])):
        #        f.write(','+str(int(sorted(list(levels[yl2]))[l]==ls1)))
        #    for l in range(len(levels[yl2])):
        #        f.write(','+str(int(sorted(list(levels[yl2]))[l]==mf1)))
        f.write('\n')
f.close()
