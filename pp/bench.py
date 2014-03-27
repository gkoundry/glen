#f=open('train.csv','r')
f=open('trains.csv','r')
c=0
d=0
t=0
all_af=[]
h=f.readline()
for l in f:
    a=l.rstrip().split(',')
    rt=int(a[2])
    af=a[17:24]
    if rt==1:
        print a[0]+' '+''.join(af)+' '+''.join(last_af)
        if af==last_af:
            c+=1
        if af in all_af:
            d+=1
        all_af=[]
        t+=1
    else:
        all_af.append(af)
    last_af=af
print c*1.0/t
print d*1.0/t

