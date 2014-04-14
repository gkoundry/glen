import cPickle
import sys
from collections import defaultdict

iter='4'
pred={}
pred['A']=cPickle.load(open('predA'+iter+'.out','rb'))
pred['B']=cPickle.load(open('predB'+iter+'.out','rb'))
pred['C']=cPickle.load(open('predC'+iter+'.out','rb'))
pred['D']=cPickle.load(open('predD'+iter+'.out','rb'))
pred['E']=cPickle.load(open('predE'+iter+'.out','rb'))
pred['F']=cPickle.load(open('predF'+iter+'.out','rb'))
pred['G']=cPickle.load(open('predG'+iter+'.out','rb'))
f=open('trains3.csv','r')
h=f.readline()
afix=0
anoef1=0
abrk=0
anoef2=0
brk=0
nth=0
fix=0
ap=0
an=0
al=0
al1=0
al2=0
al3=defaultdict(int)
ic=0
ic1=0
c=0
t=0
c1=0
t1=0
sm=0
mt=0
pac=0
nac=0
lac=0
icorp=0
icorl=0
icorn=0
dw = defaultdict(int)
icd=defaultdict(int)
icr=defaultdict(int)
icd1=defaultdict(int)
for l in f:
    a=l.rstrip().split(',')
    if a[2]=='1':
        id = str(int(a[0]))
        p = []
        pl = []
        for i in ('A','B','C','D','E','F','G'):
            pl.append(lasta[ord(i)-65+17])
            if id in pred[i]:
                if i=='A':
                    p.append(str(int(pred[i][id])))
                else:
                    p.append(lasta[ord(i)-65+17])
            else:
                print id
                sys.exit(0)
                p.append(lasta[ord(i)-65+17])
            if p[-1]==a[ord(i)-65+17] and id in pred[i]:
                mt += 1
            if p[-1]!=pl[-1]:
                if p[-1]==a[ord(i)-65+17]:
                    ic += 1
                    icd[i] += 1
                else:
                    icr[i] += 1
            if pl[-1] != p[-1]:
                if p[-1]==a[ord(i)-65+17]:
                    icorp += 1
                elif pl[-1]==a[ord(i)-65+17]:
                    icorl += 1
                else:
                    icorn += 1
            if pl[-1]==a[ord(i)-65+17]:
                ic1 += 1
                icd1[i] += 1

#        if p!=pl:
#            print '%-12s %s %s %s %d %d' % (id,a[17:24],pl,p,a[17:24]==pl,a[17:24]==p)
        if pl!=p:
            if pl==a[17:24]:
                brk += 1
            if p==a[17:24]:
                fix += 1
            if p==a[17:24]:
                nth += 1

#        for i in range(7):
#            if p[i]!=pl[i]:
#                print '%-12s %s %s %s %d %d' % (id,a[17:24],pl,p,p[i]==a[i+17],a[17:24]==p)
        if a[17:24]==p:
            c+=1
        if a[17:24]==pl:
            c1+=1
        if p[0]!=pl[0]:
            if p[0]==a[17]:
                if p==a[17:24]:
                    afix+=1
                else:
                    anoef1+=1
            else:
                if pl==a[17:24]:
                    print '%d %-12s %s %s %s' % (p==a[17:24],id,a[17:24],pl,p)
                    abrk+=1
                else:
                    anoef2+=1
        if p[0]!=pl[0]:
            if a[17:24]==p:
                ap += 1
            elif a[17:24]==pl:
                al += 1
            else:
                an += 1
                if a[17]==p[0]:
                    for i in range(7):
                        if a[17+i]!=p[i]:
                            al3[i] += 1
                    al1+=1
                else:
                    al2+=1
        if p==pl:
            sm+=1
        else:
            if a[17:24]!=p:
                for i in range(17,24):
                    if a[i]!=p[i-17]:
                        dw[chr(48+i)]+=1
            if a[17:24]==p:
                pac+=1
            elif a[17:24]==pl:
                lac+=1
            else:
                nac+=1
        #print str(a[17:24])
        #print ' '+str(pl)
        #print ' '+str(p)
        t+=1
    lasta=a
print c*1.0/t
print c1*1.0/t
print str(c1)+' '+str(t)
print sm
print ic*1.0/(7*t)
print ic1*1.0/(7*t)
print mt
for i in ('A','B','C','D','E','F','G'):
    print i+' '+str(icd[i])+' '+str(icd1[i])+' '+str(icd[i]-icd1[i])+' '+str(icr[i])
print '%d %d %d' % (pac,lac,nac)
print '%d %d %d' % (icorp,icorl,icorn)
print dw
print '%d %d %d %d %d' % (ap,al,an,al1,al2)
print al3
print 'brk %d fix %d nth %d' % (brk,fix,nth)
print 'afix %d anoef1 %d abrk %d anoef2 %d' % (afix,anoef1,abrk,anoef2)
