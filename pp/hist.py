from collections import defaultdict
f=open('test.csv','r')
#f=open('train.csv','r')
#f=open('trains.csv','r')
h=f.readline()
count=defaultdict(int)
hist=defaultdict(int)
tot=0
for l in f:
    a=l.rstrip().split(',')
    id=int(a[0])
    rt=a[2]
    if rt=='0':
        count[id]+=1
        tot+=1
med=[]
for c in count.values():
    hist[c]+=1
    med.append(c)
print 'med='+str(sorted(med)[len(med)/2])+' avg='+str(sum(med)*1.0/len(med))
for c in sorted(hist.keys()):
    print '%2d %12.8f' % (c,hist[c]*1.0/tot)
