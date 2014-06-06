from collections import defaultdict
f=open('training.csv','r')
h=f.readline().rstrip().split(',')
freq=defaultdict(int)
cnt=defaultdict(int)
for l in f:
    a=l.rstrip().split(',')
    if a[32]=='s':
        freq[a[23]]+=1
    cnt[a[23]]+=1
for i,j in cnt.items():
    print '%s %s %s' % (i,j,freq[i]*1.0/j)
