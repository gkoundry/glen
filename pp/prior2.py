import sys
from math import log
from collections import defaultdict

f=open('trains.csv','r')
h=f.readline()
tfreq={}
freq={}
for i in range(7):
    tfreq[i] = defaultdict(int)
    freq[i] = {}
    for j in range(7):
        freq[i][str(j)] = defaultdict(int)

for l in f:
    a=l.rstrip().split(',')
    rt=int(a[2])
    if rt==1:
        for v in (17,18,19,20,21,22,23):
            for w in (17,18,19,20,21,22,23):
                freq[v-17][a[v]][a[w]] += 1
                tfreq[v-17][a[v]] += 1

f=open('trains.csv','r')
h=f.readline()
for l in f:
    a=l.rstrip().split(',')
    rt=int(a[2])
    if rt==1:
        sys.stdout.write(''.join(a[17:24]))
        pp = 0
        for y in range(7):
            p = 0
            for z in range(7):
                if y != z:
                    p += log(freq[y][a[17+y]][a[17+z]]*1.0/tfreq[y][a[17+y]])
            sys.stdout.write(' '+str(p))
            pp += p
        sys.stdout.write(" %f\n" % pp)
