pred = {}
pred['G']={}
for col in ('A','B','C','D','E','F'):
    f=open('pred'+col+'G.csv','r')
    pred[col]={}
    for l in f:
        id,p = l.rstrip().split(',')
        id=int(id)
        if id not in pred['G']:
            pred['G'][id]=[]
        pred['G'][id].append(p[1])
        pred[col][id]=p[0]

f=open('trains1.csv','r')
h=f.readline()
scp=0
scl=0
tot=0
for l in f:
    a=l.rstrip().split(',')
    if a[2]=='1':
        c=1
        cl=1
        id=int(a[0])
        for col in ('A','B','C','D','E','F','G'):
            if col=='G':
                p=pred[col][id][0]
            else:
                p=pred[col][id]
            if a[ord(col)-48] != p:
                c=0
            if a[ord(col)-48] != lasta[ord(col)-48]:
                cl=0
        if c==1:
            scp+=1
        if cl==1:
            scl+=1
        tot+=1
    lasta=a
print '%d %d %d' % (scp,scl,tot)
