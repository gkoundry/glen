import sys

f=open(sys.argv[1],'r')
cc = 0
for l in f:
    a = l.rstrip().split()
    for b in a[1:]:
        col,v = b.split(':')
        if int(col)>cc:
            cc=int(col)
print 'y,'+','.join(['V%d' % (i+1) for i in range(cc)])
f=open(sys.argv[1],'r')
for l in f:
    a = l.rstrip().split()
    out = [a[0]]+['']*cc
    for b in a[1:]:
        col,v = b.split(':')
        out[int(col)] = v
    print ','.join(out)
