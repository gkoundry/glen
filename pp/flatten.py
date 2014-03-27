import sys
f=open('trains.csv','r')
h=f.readline()
out={}
y={}
lmax=0
for l in f:
    a=l.rstrip().split(',')
    id=a[0]
    rt=a[2]
    if id not in out:
        out[id]=[]
    if rt=='1':
        y[id]=a[17:24]
    else:
        for v in (24,23,22,21,20,19,18,17):
            out[id] = [a[v]]+out[id]
        if len(out[id])>lmax:
            lmax=len(out[id])

sys.stdout.write('A,B,C,D,E,F,G')
for i in range(lmax/8):
    sys.stdout.write(',A%d,B%d,C%d,D%d,E%d,F%d,G%d,Cost%d' % (i,i,i,i,i,i,i,i))
sys.stdout.write('\n')
for k,v in out.items():
    sys.stdout.write( ','.join(y[k]))
    for i in range(lmax):
        if len(v)>i+1:
            sys.stdout.write( ','+v[i])
        else:
            sys.stdout.write( ',9')
    sys.stdout.write('\n')

