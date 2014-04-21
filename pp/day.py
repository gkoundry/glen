from collections import defaultdict
import sys
f=open('train.csv','r')
h=f.readline()
col=18
sf={}
levels=set()
for l in f:
    a=l.rstrip().split(',')
    if a[3] not in sf:
        sf[a[3]]=defaultdict(int)
    sf[a[3]][a[18]]+=1
    levels.add(a[18])
ls = sorted(list(levels))
for s,c in sf.items():
    sys.stdout.write(s)
    for l in levels:
        sys.stdout.write(',%f' % ((500+c[l]*1.0)/(500*len(ls)+sum(c.values())),))
    sys.stdout.write("\n")
