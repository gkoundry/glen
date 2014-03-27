f=open('tmp1b','r')
pa={}
for l in f:
    id,act,pred=l.rstrip().split()
    pa[id]=(act,pred)
f=open('tmp1r')
h=f.readline()
bc=0
bw=0
lc=0
rc=0
for l in f:
    id,pred=l.rstrip().split()
    id=id.replace('.0','')
    print id,pa[id][0],pa[id][1],pred
    if pa[id][0]==pa[id][1]:
        if pa[id][0]==pred:
            bc+=1
        else:
            lc+=1
    else:
        if pa[id][0]==pred:
            rc+=1
        else:
            bw+=1
print 'bc %d lc %d rc %d bw %d' % (bc,lc,rc,bw)
