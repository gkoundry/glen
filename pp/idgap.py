from collections import defaultdict

f=open('train.csv','r')
h=f.readline()
cnt={}
tot={}
for c in range(17,24):
    cnt[c]=defaultdict(int)
    tot[c]=defaultdict(int)
gap=1
oldid=''
for l in f:
    a=l.rstrip().split(',')
    id=a[0]
    if id!=oldid and oldid!='':
        gap=int(id)-int(oldid)
    rt=a[2]
    if rt=='1':
        for c in range(17,24):
            if a[c]=='1':
                cnt[c][gap]+=1
            tot[c][gap]+=1
    lasta=a
    oldid=id
for c in range(17,24):
    print chr(c+48)
    for i,j in tot[c].items():
        print ' %d %d %f' % (i,j,cnt[c][i]*1.0/j)
