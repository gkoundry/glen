f=open('training.csv','r')
f1=open('training1.csv','w')
f2=open('training2.csv','w')
f3=open('training3.csv','w')
h=f.readline()
f1.write(h)
f2.write(h)
f3.write(h)
for l in f:
    a=l.split(',')
    if a[23]=='0':
        f1.write(l)
    if a[23]=='1':
        f2.write(l)
    if a[23]=='2':
        f3.write(l)
    if a[23]=='3':
        f3.write(l)
