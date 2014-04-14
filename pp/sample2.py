import random
import numpy as np
from copy import copy
import sys
from collections import defaultdict

def check(s,c,b):
    #print str(c)+' '+str(s)+' '+str(c*p1+s*p2+p3)
    return c==1 or random.randint(0,1000)<b[s]
    #return c==1 or random.randint(0,1000)<c*p1+s*s*p2+p3

#b=[220,260,310,400,500,500,500,500,500,500,500,500,500]
#b=[220,260,350,400,500,500,500,500,500,500,500,500,490,500,500]
b=[60, 350, 330, 355, 560, 670, 665, 780, 885, 1025, 775, 820, 700, 750]
bestsc=999
random.seed(1234+135)
out=open('trainrs.csv','w')

seen = {}
so=''
for lp in range(10):
    count=defaultdict(int)
    last={}
    f=open('train.csv','r')
    h=f.readline()
    if lp==0:
        out.write(h)
    for l in f:
        a=l.rstrip().split(',')
        id=int(a[0])
        rt=a[2]
        if rt=='0':
            last[id]=int(a[1])
            count[id]+=1
    f.close()
    oldb=copy(b)
    col=np.random.randint(0,13)
    chg=np.random.randint(0,20)-10
    #b[col] += chg*5

    f=open('train.csv','r')
    h=f.readline()
    for l in f:
        a=l.rstrip().split(',')
        rt=a[2]
        id=int(a[0])
        s=last[id]-int(a[1])
        if rt=='1' or check(s,count[id],b):
            id2 = str(lp+1)+str(id)[1:]
            so += (str(lp+1)+l[1:])
            if id2 not in seen:
                seen[id2] = ''
            seen[id2] += a[1]
            if rt=='1':
                fl = 1
                for i in range(lp):
                    if seen[str(i+1)+str(id)[1:]] == seen[id2]:
                        fl=0
                        break
                if fl:
                    out.write(so)
                else:
                    count[id]-=1
                so=''
        else:
            count[id]-=1
    f.close()
out.close()
