import random
from collections import defaultdict
f=open('train.csv')
h=f.readline()
print h.rstrip()
count=defaultdict(int)
for l in f:
    a=l.rstrip().split(',')
    rt=a[2]
    if rt!='1':
        count[a[0]]+=1

rnd = {}
for ll in range(1):
    random.seed(2134+3*ll)
    f=open('train.csv')
    h=f.readline()
    oldid=''
    for l in f:
        a=l.rstrip().split(',')
        rt=a[2]
        sp=int(a[1])
        id=a[0]
        if id!=oldid:
            x=0
            if id not in rnd:
                rnd[id] = []
            t = random.randint(3,max(3,count[id]))
            while x<15 and t in rnd[id]:
                t = random.randint(3,max(3,count[id]))
                x+=1
            if t in rnd[id]:
                t = -1
            else:
                rnd[id].append(t)
        if rt=='1' and t>-1:
            print str(ll)+l.rstrip()
        else:
            if sp<t:
                print str(ll)+l.rstrip()
        oldid=id
