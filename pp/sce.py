from collections import defaultdict
f=open('tmp1e','r')
pred={}
predp={}
for l in f:
    a,b=l.rstrip().split()
    pred[int(float(a))]=int(float(b)>0.5)
    predp[int(float(a))]=float(b)

f=open('trains3.csv','r')
h=f.readline()
scp=0
scl=0
restc=defaultdict(int)
restn=defaultdict(int)
restl={}
restt={}
for i in range(7):
    restl[chr(65+i)]=defaultdict(int)
    restt[chr(65+i)]=defaultdict(int)
for l in f:
    a=l.rstrip().split(',')
    id=int(a[0])
    rt=a[2]
    if rt=='1':
        rest = 0
        for i in range(7):
            if last[17+i]==a[17+i]:
                rest+=1
        if int(last[21])!=pred[id]:
            print str(id)+' '+str(predp[id])+' '+str(pred[id]==int(a[21]))+' '+str(last[17:21]+last[22:24]==a[17:21]+a[22:24])
        if pred[id]==int(a[21]):
            scp += 1
            if int(last[21])!=pred[id]:
                restc[rest]+=1
        else:
            if int(last[21])!=pred[id]:
                restn[rest]+=1
                for i in range(7):
                    restl[chr(65+i)][last[17+i]]+=1
        for i in range(7):
            restt[chr(65+i)][last[17+i]]+=1
        if last[21]==a[21]:
            scl += 1
    last=a
print '%d %d' % (scp,scl)
print 'restc %s %d' % (restc,sum(restc.values()))
print 'restn %s %d' % (restn,sum(restn.values()))
print 'restl %s' % restl
print 'restt %s' % restt
for i in ('A','B','C','D','E','F','G'):
    for j in restt[i].keys():
        print '%s %s %f' % (i,j,restl[i][j]*1.0/restt[i][j])
