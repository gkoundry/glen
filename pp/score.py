f=open('testl.out','r')
pred={}
for l in f:
    a=l.rstrip().split()
    pred[int(float(a[0]))] = [str(int(float(i))) for i in a[1:]]
f=open('trainrs.csv','r')
h=f.readline()
c=0
t=0
c1=0
t1=0
for l in f:
    a=l.rstrip().split(',')
    if a[2]=='1':
        #print a[0]+' '+str(a[17:24])+' '+str(pred[int(float(a[0]))])
        if a[17:24]==pred[int(float(a[0]))]:
            c+=1
        t+=1
        for i in range(17,24):
            if a[i]==pred[int(float(a[0]))][i-17]:
                c1+=1
            t1+=1
print c*1.0/t
print c1*1.0/t1
print str(c1)+' '+str(t1)
