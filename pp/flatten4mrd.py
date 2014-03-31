import sys
from collections import defaultdict

def mean(l):
    return sum(l)*1.0/len(l)

levels = { 'A':set(),'B':set(),'C':set(),'D':set(),'E':set(),'F':set(),'G':set() }
prior={}
age={}
ans={}
mfreq={}
lastg={}
quotes=defaultdict(int)
freq={}
last={}
llast={}
costw = {}
chist = defaultdict(list)
costdir={}
avg_co = {}
risk = {}
mrd={}
for col in ('A','B','C','D','E','F','G'):
    prior[col] = defaultdict(int)
    costw[col] = defaultdict(list)
    avg_co[col] = defaultdict(list)

f=open('trains3.csv','r')
h=f.readline()
for l in f:
    a=l.rstrip().split(',')
    id=a[0]
    rt=a[2]
    cs=float(a[24])
    if id not in age:
        age[id] = {}
        bestf = { 'A':0, 'B':0, 'C':0, 'D':0, 'E':0, 'F':0, 'G':0 }
        hist = { 'A':[-1], 'B':[-1], 'C':[-1], 'D':[-1], 'E':[-1], 'F':[-1], 'G':[-1] }
        freq[id] = {}
        mfreq[id] = {}
        last[id] = {}
        llast[id] = {}
        costdir[id] = {}
    if rt=='1':
        ans[id]={}
    else:
        quotes[id] += 1
        risk[id] = a[11]
    for col in ('A','B','C','D','E','F','G'):
        val = a[ord(col)-48]
        if col not in age[id]:
            age[id][col] = {}
            costdir[id][col] = {}
        levels[col].add(val)
        if rt=='1':
            last_val = lasta[ord(col)-48]
            lastg[id]=lasta[ord('G')-48]
            last[id][col] = last_val
            while hist[col][-1]==last_val:
                hist[col].pop()
            llast[id][col] = hist[col][-1]
            ans[id][col] = val
            prior[col][last_val]+=1
            hist[col] = [-1]
            costdir[id][col]=chist[col][-1]*1.0/(sum(chist[col][:-1])*1.0/len(chist[col][:-1]))
            if len(costw[col].keys())>1:
                for i in costw[col].keys():
                    costwo = []
                    for j in costw[col].keys():
                        if i!=j:
                            costwo.extend(costw[col][j])
                    avg_co[col][i].append(mean(costw[col][i])/mean(costwo))
            costw[col] = defaultdict(list)
            chist[col] = []
        else:
            mrd[id]=a[14]
            if col not in freq[id]:
                freq[id][col] = defaultdict(int)
            freq[id][col][val] += 1
            if freq[id][col][val] >= bestf[col]:
                bestf[col] = freq[id][col][val]
                mfreq[id][col] = val
            for k in age[id][col].keys():
                age[id][col][k] += 1
            age[id][col][val]=0
            hist[col].append(val)
            costw[col][val].append(cs)
            chist[col].append(cs)
    lasta=a

rd = {
    'NA': (1,0,0,0,0),
    '1': (0,1,0,0,0),
    '2': (0,0,1,0,0),
    '3': (0,0,0,1,0),
    '4': (0,0,0,0,1),
}
for col in ('A','B','C','D','E','F','G'):
    for i in avg_co[col].keys():
        avg_co[col][i] = mean(avg_co[col][i])
    f=open('train4'+col+'mrd.csv','w')
    f.write("id,y,ls,mf,agemf,prls,prmf,frls,frmf,quotes,nfrls,nfrmf,frrt,prrt,csls,csmf,risk0,risk1,risk2,risk3,risk4,csdir,G1,G2,G3,G4,mrd\n")
    for id in ans.keys():
        ls = last[id][col]
        #mf = mfreq[id][col]
        mf = llast[id][col]
        if mf==-1 or ans[id][col] not in (ls,mf):
        #if ls==mf or ans[id][col] not in (ls,mf):
            continue
        f.write("%s,%d,%s,%s" % (id,ls==ans[id][col],ls,mf))
        f.write(",%d,%d,%d,%d,%d,%d,%f,%f,%f,%f,%f,%f" % (age[id][col][mf],prior[col][ls],prior[col][mf],freq[id][col][ls],freq[id][col][mf],quotes[id],freq[id][col][ls]*1.0/quotes[id],freq[id][col][mf]*1.0/quotes[id],(freq[id][col][mf]+10.0)/(freq[id][col][ls]+10.0),(prior[col][mf]+10.0)/(prior[col][ls]+10.0),avg_co[col][ls],avg_co[col][mf]))
        f.write(",%s,%s,%s,%s,%s" % rd[risk[id]])
        f.write(',%f,%d,%d,%d,%d' % (costdir[id][col],int(lastg[id]=='1'),int(lastg[id]=='2'),int(lastg[id]=='3'),int(lastg[id]=='4')))
        f.write(',%s' % mrd[id])
        f.write('\n')
    f.close()

