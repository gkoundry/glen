import sys
cols = ('A','B','C','D','E','F','G')
pred = {}
for col in ('A','B','C','D','E','F','G'):
    f=open('pred'+col+'.csv','r')
    pred[col]={}
    for l in f:
        id,p = l.rstrip().split(',')
        id=int(id)
        pred[col][id]=p[1]

f=open('trains1.csv','r')
h=f.readline()
scp=0
scl=0
fix=0
brk=0
tot=0
for l in f:
    a=l.rstrip().split(',')
    if a[2]=='1':
        c=1
        cl=1
        id=int(a[0])
        pp=''
        pl=''
        for col in ('A','B','C','D','E','F','G'):
            if col in cols:
                p=pred[col][id]
            else:
                p = lasta[ord(col)-48]
            pp += p
            pl += lasta[ord(col)-48]
            if int(a[ord(col)-48]) != int(p):
                c=0
            if int(a[ord(col)-48]) != int(lasta[ord(col)-48]):
                cl=0
            #sys.stdout.write(p)
        #sys.stdout.write(" %d\n" % c)
        if c==1:
            scp+=1
        if cl==1:
            scl+=1
        if pp!=pl:
            if c==1:
                fix+=1
                print '%d %s %s 1' % (id,pl,pp)
            if cl==1:
                brk+=1
                print '%d %s %s 0' % (id,pl,pp)
        tot+=1
    lasta=a
print '%d %d %d %d %d' % (scp,scl,tot,fix,brk)
