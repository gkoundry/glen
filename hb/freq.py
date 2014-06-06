from collections import defaultdict
f=open('training.csv','r')
h=f.readline().rstrip().split(',')
freq=defaultdict(set)
for l in f:
    a=l.rstrip().split(',')
    for i,j in enumerate(a):
        freq[h[i]].add(j)
for i,j in freq.items():
    if len(j)<100:
        print '%s %s' % (i,j)
