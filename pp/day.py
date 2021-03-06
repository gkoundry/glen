from collections import defaultdict
import sys
ff=16
for col in range(17,24):
    f=open('train.csv','r')
    h=f.readline()
    sf={}
    levels=set()
    for l in f:
        a=l.rstrip().split(',')
        if a[ff] not in sf:
            sf[a[ff]]=defaultdict(int)
        sf[a[ff]][a[col]]+=1
        levels.add(a[col])
    ls = sorted(list(levels))
    for s,c in sf.items():
        sys.stdout.write(chr(col+48)+','+s)
        for l in levels:
            sys.stdout.write(',%f' % ((500+c[l]*1.0)/(500*len(ls)+sum(c.values())),))
        sys.stdout.write("\n")
