import sys
test = open(sys.argv[1],'r')
act = open(sys.argv[2],'r')
pred = open(sys.argv[3],'r')
neg=0
tot=0
for t in test:
    a=t.split()
    if a[0]=='-1':
        neg+=1
    tot += 1
neg = neg * 1.0 / tot
sc=0
c=0
i=0
pl=[]
p = pred.readline().rstrip()
for p in pred:
    p = float(p.split(',')[1])
    pl.append([i,p,1])
    i+=1

pl = sorted(pl,key=lambda x:x[1])
pl2 = []
th=1
for i,p in enumerate(pl):
    if i*1.0/len(pl)<neg:
        #pl[i][2] == -1
        pl2.append([pl[i][0],pl[i][1],-1])
    else:
        if th:
            th=0
            print 'Thresh %f' % (pl[i][1],)
        pl2.append([pl[i][0],pl[i][1],1])
pl2 = sorted(pl2,key=lambda x:x[0])
print '\n'.join([str(i) for i in pl2])

for i,a in enumerate(act):
    af = a.split()
    a = float(af[0])
    sc += int(a!=pl2[i][2])
    c +=1
print sc*1.0/c

