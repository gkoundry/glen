from collections import defaultdict

f=open('train.csv','r')
#f=open('trains3.csv','r')
h=f.readline()
tot=0
ml=0
nml=0
lo=0
nlo=0
mflls=0
mfc=0
hmg=0
lls=0
nth=0
oth=0
hist=defaultdict(list)
mfreq=defaultdict(list)
best=defaultdict(int)
freq = {}
for c in range(17,24):
    freq[c] = defaultdict(int)
for l in f:
    a=l.rstrip().split(',')
    id=a[0]
    rt=a[2]
    if rt=='1':
        for c in range(17,24):
            tot+=1
            if a[c]!=lasta[c]:
                nml+=1
                nf = a[c] in hist[c]
                while len(hist[c])>0:
                    ls = hist[c].pop()
                    if ls!=lasta[c]:
                        break
                if ls!=lasta[c]:
                    nlo+=1
                    mf = mfreq[c][-1]
                    #print id+' '+chr(c+48)+' '+str(a[c])+' '+str(lasta[c])+' '+str(ls)+' '+str(mf)
                    if mf==ls and a[c]==ls:
                        mflls+=1
                    elif a[c]==mf:
                        mfc+=1
                    elif a[c]==ls:
                        lls+=1
                    elif nf:
                        oth+=1
                    else:
                        nth+=1
                else:
                    lo+=1
            else:
                ml+=1
                if all([lasta[c]==j for j in hist[c]]):
                    hmg+=1
            hist[c] = []
            best[c] = 0
            freq[c] = defaultdict(int)
    else:

        for c in range(17,24):
            hist[c].append(a[c])
            freq[c][a[c]] += 1
            if freq[c][a[c]] > best[c]:
                best[c] = freq[c][a[c]]
                mfreq[c] = []
            if freq[c][a[c]] >= best[c]:
                mfreq[c].append(a[c])

    lasta=a

print 'tot %d' % tot
print ' ml  %d' % ml
print '  hmg %d' % hmg
print ' nml %d' % nml
print '  lo  %d' % lo
print '  nlo  %d' % nlo
print '   mflls %s' % mflls
print '   lls %s' % lls
print '   mf %s' % mfc
print '   oth %s' % oth
print '   nth %s' % nth
