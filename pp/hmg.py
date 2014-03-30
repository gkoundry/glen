from collections import defaultdict
import sys

hist=defaultdict(list)
freq=defaultdict(int)
f=open('train.csv','r')
h=f.readline()
hmg={}
for l in f:
    a=l.rstrip().split(',')
    id=a[0]
    rt=a[2]
    for c in range(17,24):
        if len(set(hist[c]))==1:
            hmg[c]=True
        else:
            hmg[c]=False
        hist[c].append(a[c])
    if rt=='1':
        for c in range(17,24):
            if lasta[c] != a[c]:
                hist[c].reverse()
                if hmg[c]:
                    sys.stdout.write('*')
                    freq[chr(c+48)+a[c]+lasta[c]]+=1
                else:
                    sys.stdout.write(' ')
                print id+' '+chr(c+48)+' '+''.join(hist[c])
            hist[c] = []
    lasta=a
for i,j in freq.items():
    print '%s %d' % (i,j)
