
f=open('train.csv','r')
hdr = f.readline().rstrip().split(',')
print 'ans,l_ans,y,'+','.join(hdr[3:])
for line in f:
    a = line.rstrip().split(',')
    if a[2]=='1':
        lasta[4] = str(int(lasta[4][:2]) * 60 + int(lasta[4][3:]))
        lasta[5] = str((ord(lasta[5][0])-65) *26+ord(lasta[5][1]))
        if lasta[10] == '':
            lasta[10]='c'
        lasta[10] = str(ord(lasta[10]))
        if lasta[11]=='NA':
            lasta[11]='2'
        if lasta[15]=='NA':
            lasta[15]='2'
        if lasta[16]=='NA':
            lasta[16]='2'
        print ''.join(a[17:24])+','+''.join(lasta[17:24])+','+a[21]+','+','.join(lasta[3:])
    lasta = a
