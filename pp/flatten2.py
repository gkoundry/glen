import sys
from collections import defaultdict
f=open('trains.csv','r')
h=f.readline()
count={}
quotes={}
levels = { 'A':set(),'B':set(),'C':set(),'D':set(),'E':set(),'F':set(),'G':set() }
last={}
y={}
lmax=0
for l in f:
    a=l.rstrip().split(',')
    id=a[0]
    rt=a[2]
    if id not in count:
        count[id]= defaultdict(int)
        quotes[id] = 0
        last[id] = defaultdict(int)
    if rt=='1':
        y[id]=a[17:24]
        for v in (17,18,19,20,21,22,23):
            last[id][chr(v+48)+lasta[v]] = 2
    else:
        quotes[id] += 1
        lasta = a
        for v in (17,18,19,20,21,22,23):
            levels[chr(v+48)].add(a[v])
            count[id][chr(v+48)+a[v]] += 1
            last[id][chr(v+48)+a[v]] = 1

sys.stdout.write('id,A,B,C,D,E,F,G')
for o in ('A','B','C','D','E','F','G'):
    for l in sorted(list(levels[o])):
        sys.stdout.write(',cnt_%s%s' % (o,l))
    for l in sorted(list(levels[o])):
        sys.stdout.write(',lst_%s%s' % (o,l))
sys.stdout.write('\n')
for k in y.keys():
    sys.stdout.write(k+','+','.join(y[k]))
    for o in ('A','B','C','D','E','F','G'):
        for l in sorted(list(levels[o])):
            sys.stdout.write(',%f' % count[k][o+l])
            #sys.stdout.write(',%f' % (count[k][o+l]*1.0/quotes[k]))
        for l in sorted(list(levels[o])):
            sys.stdout.write(',%d' % last[k][o+l])
    sys.stdout.write('\n')

