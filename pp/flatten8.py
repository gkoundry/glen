
f=open('trains1.csv','r')
hdr = f.readline().rstrip().split(',')
print 'ans,l_ans,y,'+','.join(hdr[3:])+','+','.join(['l'+i for i in hdr[3:]])
lasta=None
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
        lastaa[4] = str(int(lastaa[4][:2]) * 60 + int(lastaa[4][3:]))
        lastaa[5] = str((ord(lastaa[5][0])-65) *26+ord(lastaa[5][1]))
        if lastaa[10] == '':
            lastaa[10]='c'
        lastaa[10] = str(ord(lastaa[10]))
        if lastaa[11]=='NA':
            lastaa[11]='2'
        if lastaa[15]=='NA':
            lastaa[15]='2'
        if lastaa[16]=='NA':
            lastaa[16]='2'
        print ''.join(a[17:24])+','+''.join(lasta[17:24])+','+a[21]+','+','.join(lasta[3:])+','+','.join(lastaa[3:])
    lastaa = lasta
    lasta = a
