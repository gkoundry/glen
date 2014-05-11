import sys
act = open(sys.argv[1],'r')
pred = open(sys.argv[2],'r')
sc=0
c=0
for a in act:
    pl = pred.readline().rstrip()
    if 'predicted' in pl:
        pl = pred.readline().rstrip()
    if ',' in pl:
        p = float(pl.split(',')[1])
    else:
        p = float(pl)
    af = a.split()
    a = float(af[0])
    sc += int((a+1)/2!=(p>0.5))
    c +=1
print sc*1.0/c
