from collections import defaultdict
f=open('tmp7b','r')
imp=defaultdict(list)
for l in f:
    v,i = l.rstrip().split()
    imp[v].append(i)
for i,j in imp.items():
    print '%s %f %s' % (i,min(map(float,j)),' '.join(j))
