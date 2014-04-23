import sys
import cPickle
from collections import defaultdict

if len(sys.argv)>1:
    target1=sys.argv[1]
else:
    target1 = 'G'

def mean(l):
    return sum(l)*1.0/len(l)
def tval(c):
    return ord(c)-65
def carval(v):
    if v=='':
        return (0,1)
    else:
        return (ord(v)-ord('a')+1,0)
def rfx(v):
    if v=='NA':
        return (0,1)
    else:
        return (v,0)

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
mc={}
ao={}
ad={}
cv={}
cvm={}
rf={}
rfm={}
cp={}
hist={}
cpm={}
dp={}
dpm={}
state={}
prior={}
lcost={}
states = set()
for col in ('A','B','C','D','E','F','G'):
    prior[col]=defaultdict(int)
tcost=0
ccost=0
day={}
hour={}
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
        gs[id]=a[7]
        ho[id]=a[8]
        ca[id]=a[9]
        dp[id]=a[16]
        mc[id]=a[14]
        ao[id]=a[12]
        cv[id],cvm[id] = carval(a[10])
        rf[id],rfm[id] = rfx(a[11])
        cp[id],cpm[id] = rfx(a[15])
        dp[id],dpm[id] = rfx(a[16])
        day[id]=a[3]
        hour[id]=a[4].split(':')[0]
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
            hist[id] = {}
            for col in ('A','B','C','D','E','F','G'):
                freq[id][col] = defaultdict(int)
                lcost[id][col]=defaultdict(int)
                hist[id][col]=defaultdict(int)
        for col in ('A','B','C','D','E','F','G'):
            freq[id][col][a[ord(col)-48]] += 1
            lcost[id][col][a[ord(col)-48]] += cs
            prior[col][a[ord(col)-48]] += 1
            if id in last and a[ord(col)-48] == last[id][ord(col)-65]:
                hist[id][col] += 1
            else:
                hist[id][col]=1
        last[id] = a[17:24]

f=open('train9'+target1+'.csv','w')
f.write('id,y,ls,ans,last,rest')
for col in ('A','B','C','D','E','F','G'):
    for lvl in sorted(list(levels[col])):
        f.write(',last'+col+lvl)
for lvl in sorted(list(levels[target1])):
    f.write(',freq'+target1+lvl)
for col in ('A','B','C','D','E','F','G'):
    f.write(',hist'+col)
f.write(',gs')
f.write(',ho')
f.write(',ca')
f.write(',dp')
f.write(',mc')
f.write(',ao')
f.write(',ad')
f.write(',costlvl')
f.write(',costdir')
f.write(',quotes')
f.write(',day5')
f.write(',day6')
f.write(',hour')
f.write(',cv')
f.write(',cvm')
f.write(',rf')
f.write(',rfm')
f.write(',cp')
f.write(',cpm')
f.write(',dp')
f.write(',dpm')
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
    for col in ('A','B','C','D','E','F','G'):
        f.write(',%d' % hist[id][col])
    f.write(',%s' % gs[id])
    f.write(',%s' % ho[id])
    f.write(',%s' % ca[id])
    f.write(',%s' % dp[id])
    f.write(',%s' % mc[id])
    f.write(',%s' % ao[id])
    f.write(',%s' % ad[id])
    f.write(',%f' % costlvl[id])
    f.write(',%f' % costdir[id])
    f.write(',%d' % quotes[id])
    f.write(',%d' % int(day[id]=='5'))
    f.write(',%d' % int(day[id]=='6'))
    f.write(',%s' % hour[id])
    f.write(',%s' % cv[id])
    f.write(',%s' % cvm[id])
    f.write(',%s' % rf[id])
    f.write(',%s' % rfm[id])
    f.write(',%s' % cp[id])
    f.write(',%s' % cpm[id])
    f.write(',%s' % dp[id])
    f.write(',%s' % dpm[id])
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
