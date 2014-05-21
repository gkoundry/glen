f=open('predxgbp.csv','r')
pred={}
for l in f:
    a=l.rstrip().split(',')
    pred[a[0]]=float(a[1])
f=open('predlr1p.csv','r')
pp=[]
for l in f:
    a=l.rstrip().split(',')
    p=(float(a[1])*0.1+0.9*pred[a[0]])/2
    pp.append((a[0],p))
r=1
print 'EventId,RankOrder,Class'
for i in sorted(pp,key=lambda x:-x[1]):
    print '%s,%d,%s' % (i[0],r,'s' if i[1]>1.4 else 'b')
    r+=1
