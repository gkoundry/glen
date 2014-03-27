f=open('trains.csv','r')
col1 = 0
col2 = 2
count = {}
h=f.readline()
for l in f:
    a=l.rstrip().split(',')
    if a[2]=='1':
        a1=a[17+col1]
        a2=a[17+col2]
        if a1 not in count:
            count[a1] = {}
        if a2 not in count[a1]:
            count[a1][a2] = 0
        count[a1][a2] += 1
for a1 in sorted(count.keys()):
    tot = 0
    for a2 in sorted(count[a1].keys()):
        tot += count[a1][a2]
    for a2 in sorted(count[a1].keys()):
        print a1+' '+a2+' '+str(count[a1][a2]*1.0/tot)
    print str(tot)+'\n'

