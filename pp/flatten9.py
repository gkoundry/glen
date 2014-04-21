import sys
import cPickle
from collections import defaultdict

if len(sys.argv)>1:
    target1=sys.argv[1]
else:
    target1 = 'E'

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
state={}
prior={}
lcost={}
states = set()
for col in ('A','B','C','D','E','F','G'):
    prior[col]=defaultdict(int)
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
        states.add(a[5])
        state[id]=a[5]
        ad[id]=int(a[12])-int(a[13])
        quotes[id] += 1
        if tcost > 0:
            costdir[id] = cs / (tcost/ccost)
        tcost += cs
        ccost += 1
        costlvl[id] = tcost / ccost
        if id not in freq:
            freq[id] = {}
            lcost[id] = {}
            for col in ('A','B','C','D','E','F','G'):
                freq[id][col] = defaultdict(int)
                lcost[id][col]=defaultdict(int)
        for col in ('A','B','C','D','E','F','G'):
            freq[id][col][a[ord(col)-48]] += 1
            lcost[id][col][a[ord(col)-48]] += cs
            prior[col][a[ord(col)-48]] += 1

f=open('train9'+target1+'.csv','w')
f.write('id,y,ls,ans,last,rest')
for col in ('A','B','C','D','E','F','G'):
    for lvl in sorted(list(levels[col])):
        f.write(',last'+col+lvl)
for lvl in sorted(list(levels[target1])):
    f.write(',freq'+target1+lvl)
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
for st in sorted(list(states)):
    f.write(',%s' % st)
#f.write(',csrt1')
#f.write(',csrt2')
f.write('\n')
for id in ans.keys():
    rest = 1
    for col in ('A','B','C','D','E','F','G'):
        if col!=target1 and ans[id][tval(col)]!=last[id][tval(col)]:
            rest = 0
    f.write('%s,%s,%s,%s,%s,%d' % (id,ans[id][tval(target1)],last[id][tval(target1)],''.join(ans[id]),''.join(last[id]),rest))
    for col in ('A','B','C','D','E','F','G'):
        for lvl in sorted(list(levels[col])):
            f.write(',%d' % int(last[id][tval(col)]==lvl))
    for lvl in sorted(list(levels[target1])):
        f.write(',%d' % freq[id][target1][lvl])
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
    for st in sorted(list(states)):
        f.write(',%d' % int(state[id]==st))
#    c1 = 0
#    c2 = 0
#    t1 = 0
#    t2 = 0
#    for k,v in lcost[id][target1].items():
#        if k==last[id][tval(target1)]:
#            c1 += v
#            t1 += 1
#            t1 += freq[id][target1][k]
#        else:
#            c2 += v
#            t2 += 1
#            t2 += freq[id][target1][k]
#    if c2==0:
#        c2=c1
#        t2=t1
#    f.write(',%f' % ((c1*1.0/t1)/(c2*1.0/t2)))
#    c1 = 0
#    c2 = 0
#    t1 = 0
#    t2 = 0
#    for k,v in lcost[id][target2].items():
#        if k==last[id][tval(target2)]:
#            c1 += v
#            t1 += freq[id][target2][k]
#        else:
#            c2 += v
#            t2 += freq[id][target2][k]
#    if c2==0:
#        c2=c1
#        t2=t1
#    f.write(',%f' % ((c1*1.0/t1)/(c2*1.0/t2),))
    f.write('\n')
