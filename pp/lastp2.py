from collections import defaultdict
f=open('trains.csv','r')
c1=0
t1=0
c2=0
t2=0
for l in f:
    a=l.rstrip().split(',')
    id=a[0]
    rt=a[2]
    if rt=='1':
        h1,m1=last[4].split(':')
        tm1 = int(last[3])*24*60+int(h1)*60+int(m1)
        h2,m2=a[4].split(':')
        tm2 = int(a[3])*24*60+int(h2)*60+int(m2)
        if(tm2-tm1>25):
            if last[17:24]==a[17:24]:
                c1+=1
            t1+=1
        else:
            if last[17:24]==a[17:24]:
                c2+=1
            t2+=1
    else:
        last=a
print '%d %f' % (t1,c1*1.0/t1)
print '%d %f' % (t2,c2*1.0/t2)
print (c1+c2)*1.0/(t1+t2)
