from collections import defaultdict
f=open('train.csv','r')
cnt=defaultdict(int)
tot=defaultdict(int)
for l in f:
    a=l.rstrip().split(',')
    id=a[0]
    rt=a[2]
    if rt=='1':
        for c in (18,19,20,21,22,23):
            cnt[chr(c+48)+lasta[c]]+=int(a[17]==lasta[17])
            tot[chr(c+48)+lasta[c]]+=1
    lasta=a
for i,j in tot.items():
    print '%s %d %f' % (i,j,cnt[i]*1.0/j)
