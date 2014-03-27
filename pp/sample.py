import random
import sys
from collections import defaultdict

f=open('train.csv','r')
h=f.readline()
count=defaultdict(int)
last={}
for l in f:
    a=l.rstrip().split(',')
    id=int(a[0])
    rt=a[2]
    if rt=='0':
        last[id]=int(a[1])
        count[id]+=1
f.close()

def check(s,c,p1,p2,p3):
    #print str(c)+' '+str(s)+' '+str(c*p1+s*p2+p3)
    return c==1 or random.randint(0,1000)<c*p1+s*p2+p3

while True:
    p1=random.randint(-200,200)+random.randint(-200,200)
    p2=random.randint(-500,200)+random.randint(-500,200)
    p3=random.randint(-500,100)+random.randint(-500,100)
    f=open('train.csv','r')
    out=open('trains.csv','w')
    h=f.readline()
    out.write(h)
    for l in f:
        a=l.rstrip().split(',')
        rt=a[2]
        id=int(a[0])
        s=int(a[1])-last[id]
        if rt=='1' or check(s,count[id],p1,p2,p3):
            out.write(l)
        else:
            count[id]-=1
    f.close()
    out.close()

    f=open('trains.csv','r')
    c=0
    t=0
    h=f.readline()
    for l in f:
        a=l.rstrip().split(',')
        rt=int(a[2])
        af=a[17:24]
        if rt==1:
            if af==last_af:
                c+=1
            t+=1
        last_af=af
    pred = c*1.0/t

    f=open('trains.csv','r')
    h=f.readline()
    count=defaultdict(int)
    hist=defaultdict(int)
    tot=0
    for l in f:
        a=l.rstrip().split(',')
        id=int(a[0])
        rt=a[2]
        if rt=='0':
            count[id]+=1
            tot+=1
    med=[]
    for c in count.values():
        hist[c]+=1
        med.append(c)
    if len(med)>0:
        avg=sum(med)*1.0/len(med)
        if abs(avg-2.56) < 1 and abs(pred-.54) < 0.1 and 1 in hist and 2 in hist and hist[1]>hist[2]:
            print '%d %d %d' % (p1,p2,p3)
            print 'med='+str(sorted(med)[len(med)/2])+' avg='+str(avg)+' pred='+str(pred)
            for c in sorted(hist.keys()):
                print '%2d %12.8f' % (c,hist[c]*1.0/tot)
            f.close()
            sys.stdout.flush()
