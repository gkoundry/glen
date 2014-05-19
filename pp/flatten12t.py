import sys
import cPickle
from collections import defaultdict

if len(sys.argv)>1:
    target=sys.argv[1]
else:
    target = 'D'

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
def cvt(t):
    h,m = t.split(':')
    return int(h)*60+int(m)
def tdiff(t1,t2):
    if t1<=t2:
        return t2-t1
    return t2+24*60-t1
def avg(d):
    tot=0
    cnt=0
    for k,v in d.items():
        tot+=int(k)*v
        cnt+=v
    return tot*1.0/cnt

levels = { 'A':set(),'B':set(),'C':set(),'D':set(),'E':set(),'F':set(),'G':set() }

last = {}
llast = {}
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
cost1={}
cost2={}
wavg={}
wtot={}
uniq={}
lastid=None
states = set()
for col in ('A','B','C','D','E','F','G'):
    prior[col]=defaultdict(int)
tcost=0
ccost=0
day={}
hour={}
time1={}
time2={}
quotes = defaultdict(int)
#f=open('trains1.csv','r')
f=open('test_v2.csv','r')
h=f.readline()
for l in f:
    a=l.rstrip().split(',')
    id=a[0]

    cs=float(a[24])
    if lastid and id!=lastid:
        tcost = 0
        ccost = 0
    for col in ('A','B','C','D','E','F','G'):
        val = a[ord(col)-48]
        levels[col].add(val)
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
    if id not in time1:
        time1[id] = cvt(a[4])
    time2[id] = cvt(a[4])
    if id not in cost1:
        cost1[id] = cs
        cost2[id] = cs
    else:
        if cs>cost2[id]:
            cost2[id]=cs
        if cs<cost1[id]:
            cost1[id]=cs
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
        uniq[id] = {}
        wavg[id]=defaultdict(float)
        wtot[id]=defaultdict(int)
        for col in ('A','B','C','D','E','F','G'):
            uniq[id][col] = set()
            freq[id][col] = defaultdict(int)
            lcost[id][col]=defaultdict(int)
            hist[id][col]=defaultdict(int)
    for col in ('A','B','C','D','E','F','G'):
        wavg[id][col]+=int(a[ord(col)-48])*(2**int(a[1]))
        wtot[id][col]+=(2**int(a[1]))
        uniq[id][col].add(a[ord(col)-48])
        freq[id][col][a[ord(col)-48]] += 1
        lcost[id][col][a[ord(col)-48]] += cs
        prior[col][a[ord(col)-48]] += 1
        if id in last and a[ord(col)-48] == last[id][ord(col)-65]:
            hist[id][col] += 1
        else:
            hist[id][col]=1
    if id in last:
        llast[id] = last[id][:]
    last[id] = a[17:24]
    lastid=id

f=open('train12t'+target+'.csv','w')
f.write('id,ls,last')
for col in ('A','B','C','D','E','F','G'):
    for lvl in sorted(list(levels[col])):
        f.write(',last'+col+lvl)
for col in ('A','B','C','D','E','F','G'):
    for lvl in sorted(list(levels[col])):
        f.write(',llast'+col+lvl)
for lvl in sorted(list(levels[target])):
    f.write(',freq'+target+lvl)
for col in ('A','B','C','D','E','F','G'):
    f.write(',hist'+col)
for col in ('A','B','C','D','E','F','G'):
    f.write(',uniq'+col)
f.write(',gs')
f.write(',ho')
f.write(',ca')
f.write(',dp')
f.write(',mc')
f.write(',ao')
f.write(',ad')
f.write(',costlvl')
f.write(',costdir')
f.write(',costdiff')
f.write(',quotes')
f.write(',day5')
f.write(',day6')
f.write(',hour')
f.write(',time_diff')
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
for col in ('A','B','C','D','E','F','G'):
    f.write(',avg%s' % col)
#f.write(',csrt1')
#f.write(',csrt2')
f.write('\n')
for id in ca.keys():
    f.write('%s,%s,%s' % (id,last[id][tval(target)],''.join(last[id])))
    for col in ('A','B','C','D','E','F','G'):
        for lvl in sorted(list(levels[col])):
            f.write(',%d' % int(last[id][tval(col)]==lvl))
    for col in ('A','B','C','D','E','F','G'):
        for lvl in sorted(list(levels[col])):
            f.write(',%d' % int(llast[id][tval(col)]==lvl))
    for lvl in sorted(list(levels[target])):
        f.write(',%d' % freq[id][target][lvl])
    for col in ('A','B','C','D','E','F','G'):
        f.write(',%d' % hist[id][col])
    for col in ('A','B','C','D','E','F','G'):
        f.write(',%d' % len(uniq[id][col]))
    f.write(',%s' % gs[id])
    f.write(',%s' % ho[id])
    f.write(',%s' % ca[id])
    f.write(',%s' % dp[id])
    f.write(',%s' % mc[id])
    f.write(',%s' % ao[id])
    f.write(',%s' % ad[id])
    f.write(',%f' % costlvl[id])
    f.write(',%f' % costdir[id])
    f.write(',%f' % (cost2[id]-cost1[id]))
    f.write(',%d' % quotes[id])
    f.write(',%d' % int(day[id]=='5'))
    f.write(',%d' % int(day[id]=='6'))
    f.write(',%s' % hour[id])
    f.write(',%d' % tdiff(time1[id],time2[id]))
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
    for col in ('A','B','C','D','E','F','G'):
        f.write(',%f' % (wavg[id][col]/wtot[id][col]))
        #f.write(',%f' % avg(freq[id][col]))
#    c1 = 0
#    c2 = 0
#    t1 = 0
#    t2 = 0
#    for k,v in lcost[id][target].items():
#        if k==last[id][tval(target)]:
#            c1 += v
#            t1 += 1
#            t1 += freq[id][target][k]
#        else:
#            c2 += v
#            t2 += 1
#            t2 += freq[id][target][k]
#    if c2==0:
#        c2=c1
#        t2=t1
#    f.write(',%f' % ((c1*1.0/t1)/(c2*1.0/t2)))
#    c1 = 0
#    c2 = 0
#    t1 = 0
#    t2 = 0
#    for k,v in lcost[id][target].items():
#        if k==last[id][tval(target)]:
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
