import sys
act = open(sys.argv[1],'r')
pred = open(sys.argv[2],'r')
sc=0
c=0
for a in act:
    pl = pred.readline().rstrip()
    if 'RowId' in pl:
        pl = pred.readline().rstrip()
    if ',' in pl:
        p = float(pl.split(',')[1])
    else:
        p = float(pl)
    af = a.split()
    a = float(af[0])
    sc += (a-p)**2
    c +=1
print sc/c
