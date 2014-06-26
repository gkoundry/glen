#f=open('predbl84000.csv','r')
f=open('predbl6_86000.csv','r')
h=f.readline()
s=[]
for l in f:
    a=l.rstrip().split(',')
    if a[2]=='s':
        s.append(a[0])

f=open('test.csv','r')
avg=0
h=f.readline()
idt=[]
for l in f:
    a=l.split(',')
    idt.append(a[0])

#f=open('testrgbmb1000_0.05_300_12.csv','r')
#f=open('testrgbmbw1000_0.05_300_12.csv','r')
f=open('testrgbmbs1000_0.05_300_12.csv','r')
h=f.readline()
pred=[]
i=0
for l in f:
    a=l.rstrip().split(',')
    pred.append([idt[i],float(a[1])])
    i+=1

#f=open('testrgbmg1000_0.05_300_12.csv','r')
#h=f.readline()
#pred=[]
#i=0
#for l in f:
#    a=l.rstrip().split(',')
#    pred.append([idt[i],-float(a[1])])
#    i+=1

#f=open('predxgbp.csv','r')
#f=open('testrfw_1000_6_10_2.000000.csv','r') #
#pred=[]
#for l in f:
#    a=l.rstrip().split(',')
#    pred.append([a[0],float(a[1])])

#f=open('test_ksvmc5.csv','r')
#h=f.readline()
#pred=[]
#for l in f:
#    a=l.rstrip().split(',')
#    pred.append([str(int(float(a[1]))),float(a[2])])

#f=open('predbl7.csv','r')
##f=open('predbl6.csv','r')
#f=open('predns.csv','r')
#f=open('pred1','r')
#h=f.readline()
#pred=[]
#for l in f:
#    a=l.rstrip().split(',')
#    pred.append([a[0],-float(a[1])])

#f=open('test_gam_ptw.csv','r') #
#h=f.readline()
#pred=[]
#for l in f:
#    a=l.rstrip().split(',')
#    pred.append([str(int(float(a[1]))),float(a[2])])

##f=open('test_gam_v1.csv','r') #
#f=open('testsvmc5.csv','r')
#h=f.readline()
#pred=[]
#for l in f:
#    a=l.rstrip().split(',')
#    pred.append([a[1],float(a[2])])

preds = [i[0] for i in sorted(pred,key=lambda x:-x[1])[:len(s)]]
print '%d/%d' % (len(set(s) & set(preds)),len(s))

