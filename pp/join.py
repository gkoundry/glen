import sys
LEVELS={
    'A': ('0','1','2'),
    'B': ('0','1'),
    'C': ('1','2','3','4'),
    'D': ('1','2','3'),
    'E': ('0','1'),
    'F': ('0','1','2','3'),
    'G': ('1','2','3','4'),
}
f=open('trainsc.csv','r')
pa={}
for l in f:
    id,pred,last,y=l.rstrip().split()
    pa[int(id)]=(last,pred,y)

f=open('train9G.csv')
h=f.readline().rstrip().split(',')
sys.stdout.write('yy')
for col in ('A','B','C','D','E','F'):
    for lvl in LEVELS[col]:
        sys.stdout.write(",%s%s" % (col,lvl))
sys.stdout.write(','+','.join(h))
sys.stdout.write('\n')
for l in f:
    a=l.rstrip().split(',')
    id=int(a[0])
    if id in pa:
        sys.stdout.write(pa[id][2])
        pred=pa[id][1]
        for col in ('A','B','C','D','E','F'):
            for lvl in LEVELS[col]:
                sys.stdout.write(',%d' % (pred[ord(col)-65]==lvl,))
        sys.stdout.write(","+",".join(a))
        sys.stdout.write("\n")
