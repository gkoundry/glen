#=open('train.csv','r')
prior={}
f=open('trains.csv','r')
h=f.readline()
for l in f:
    a=l.rstrip().split(',')
    rt=int(a[2])
    af=''.join(a[17:24])
    if rt==1:
        if af not in prior:
            prior[af] = 0
        prior[af] += 1
f.close()

f=open('train.csv','r')
c=0
d=0
e=0
t=0
all_af=[]
h=f.readline()
for l in f:
    a=l.rstrip().split(',')
    rt=int(a[2])
    af=''.join(a[17:24])
    if rt==1:
        if af==last_af:
            c+=1
        if af in all_af:
            d+=1
        all_af.reverse()
        print af
        print '\n'.join(["%s %d" % (a,prior.get(a,0)) for a in all_af])
        if max([(a,prior.get(a,1),all_af.index(a)) for a in all_af],key=lambda x:-(x[2]+1)*(x[1]/(x[1]+1.0)))[0]==af:
            e+=1
        all_af=[]
        t+=1
    else:
        all_af.append(af)
    last_af=af
print c*1.0/t
print d*1.0/t
print e*1.0/t

