from collections import defaultdict
for i in ('A','B','C','D','E','F','G'):
    f=open('train.csv','r')
    h=f.readline()
    freq={}
    freq1={}
    for j in ('A','B','C','D','E','F','G'):
        freq[j]=defaultdict(int)
        freq1[j]=defaultdict(int)
    for l in f:
        a=l.rstrip().split(',')
        if a[2]=='1':
            y = int(a[ord(i)-65+17]==lasta[ord(i)-65+17])
            for j in ('A','B','C','D','E','F','G'):
                if y:
                    freq[j][a[ord(j)-65+17]] += 1
                else:
                    freq1[j][a[ord(j)-65+17]] += 1
        lasta=a

    print i
    for j in ('A','B','C','D','E','F','G'):
        print ' '+j
        for k in freq[j].keys():
            print k+' '+str((freq[j][k]+1.0)/(freq1[j][k]+1))
