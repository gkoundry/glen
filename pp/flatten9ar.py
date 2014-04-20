import sys
import cPickle
from collections import defaultdict

def mean(l):
    return sum(l)*1.0/len(l)
def tval(c):
    return ord(c)-65

levels = { 'A':set(),'B':set(),'C':set(),'D':set(),'E':set(),'F':set(),'G':set() }

last = {}
ans = {}
ca = {}
costlvl = {}
costdir = {}
freq={}
gs={}
ho={}
ca={}
dp={}
cp={}
mc={}
ao={}
ad={}
tcost=0
ccost=0
quotes = defaultdict(int)
f=open('trains1.csv','r')
h=f.readline()
for l in f:
    a=l.rstrip().split(',')
    id=a[0]
    rt=a[2]
    cs=float(a[24])
    if rt=='1':
        ans[id] = a[17:24]
        for col in ('A','B','C','D','E','F','G'):
            val = a[ord(col)-48]
            levels[col].add(val)
        tcost = 0
        ccost = 0
    else:
        last[id] = a[17:24]
        gs[id]=a[7]
        ho[id]=a[8]
        ca[id]=a[9]
        dp[id]=a[16]
        cp[id]=a[15]
        mc[id]=a[14]
        ao[id]=a[12]
        ad[id]=int(a[12])-int(a[13])
        quotes[id] += 1
        if tcost > 0:
            costdir[id] = cs / (tcost/ccost)
        tcost += cs
        ccost += 1
        costlvl[id] = tcost / ccost
        if id not in freq:
            freq[id] = {}
            for col in ('A','B','C','D','E','F','G'):
                freq[id][col] = defaultdict(int)
        for col in ('A','B','C','D','E','F','G'):
            freq[id][col][a[ord(col)-48]] += 1

f=open('train9all.csv','w')
f.write('id,last')
for col in ('A','B','C','D','E','F','G'):
    f.write(",y"+col)
for col in ('A','B','C','D','E','F','G'):
    for lvl in sorted(list(levels[col])):
        f.write(',last'+col+lvl)
for col in ('A','B','C','D','E','F','G'):
    for lvl in sorted(list(levels[col])):
        f.write(',freq'+col+lvl)
f.write(',gs')
f.write(',ho')
f.write(',ca')
f.write(',dp')
f.write(',cp')
f.write(',mc')
f.write(',ao')
f.write(',ad')
f.write(',costlvl')
f.write(',costdir')
f.write(',quotes')
f.write('\n')
for id in ans.keys():
    f.write('%s,%s' % (id,''.join(last[id])))
    for col in ('A','B','C','D','E','F','G'):
        f.write(',%s' % (ans[id][tval(col)],))
    for col in ('A','B','C','D','E','F','G'):
        for lvl in sorted(list(levels[col])):
            f.write(',%d' % int(last[id][tval(col)]==lvl))
    for col in ('A','B','C','D','E','F','G'):
        for lvl in sorted(list(levels[col])):
            f.write(',%d' % freq[id][col][lvl])
    f.write(',%s' % gs[id])
    f.write(',%s' % ho[id])
    f.write(',%s' % ca[id])
    f.write(',%s' % dp[id])
    f.write(',%s' % cp[id])
    f.write(',%s' % mc[id])
    f.write(',%s' % ao[id])
    f.write(',%s' % ad[id])
    f.write(',%f' % costlvl[id])
    f.write(',%f' % costdir[id])
    f.write(',%d' % quotes[id])
    f.write('\n')
