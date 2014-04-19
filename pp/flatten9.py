import sys
import cPickle
from collections import defaultdict

if len(sys.argv)>1:
    target=sys.argv[1]
    iter=int(sys.argv[2])
else:
    target1 = 'G'
    target2 = 'G'
    iter = 0

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

f=open('train9'+target1+target2+'.csv','w')
f.write('id,y,ls,ans,last,rest')
for col in ('A','B','C','D','E','F','G'):
    for lvl in sorted(list(levels[col])):
        f.write(',last'+col+lvl)
for lvl in sorted(list(levels[target1])):
    f.write(',freq'+target1+lvl)
for lvl in sorted(list(levels[target2])):
    f.write(',freq'+target2+lvl)
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
    rest = 1
    for col in ('A','B','C','D','E','F','G'):
        if col!=target1 and col!=target2 and ans[id][tval(col)]!=last[id][tval(col)]:
            rest = 0
    f.write('%s,%s,%s,%s,%s,%d' % (id,ans[id][tval(target1)]+ans[id][tval(target2)],last[id][tval(target1)]+last[id][tval(target2)],''.join(ans[id]),''.join(last[id]),rest))
    for col in ('A','B','C','D','E','F','G'):
        for lvl in sorted(list(levels[col])):
            f.write(',%d' % int(last[id][tval(col)]==lvl))
    for lvl in sorted(list(levels[target1])):
        f.write(',%d' % freq[id][target1][lvl])
    for lvl in sorted(list(levels[target2])):
        f.write(',%d' % freq[id][target2][lvl])
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
