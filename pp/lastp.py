from collections import defaultdict
f=open('train.csv','r')
c=0
t=0
cy = defaultdict(int)
ty = defaultdict(int)
cp = defaultdict(int)
tp = defaultdict(int)
for l in f:
    a=l.rstrip().split(',')
    id=a[0]
    rt=a[2]
    if rt=='1':
        if last==a[17:24]:
            c+=1
            cp[''.join(a[17:24])]+=1
        for y in range(17,24):
            if last[y-17]==a[y]:
                cy[chr(y+48)+last[y-17]]+=1
            ty[chr(y+48)+last[y-17]]+=1
        t+=1
        tp[''.join(last)]+=1
    else:
        last=a[17:24]
print c*1.0/t
for p in tp.keys():
    print '%s %d %f' % (p,tp[p],cp[p]*1.0/tp[p])
for p in ty.keys():
    print '%s %d %f' % (p,ty[p],cy[p]*1.0/ty[p])
