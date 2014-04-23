from collections import defaultdict
f=open('tmp7i','r')
imp=defaultdict(list)
for l in f:
    v,i = l.rstrip().split()
    imp[v].append(i)
for i,j in imp.items():
    print '%s %s' % (i,' '.join(j))
