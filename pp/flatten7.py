import sys
import cPickle
from collections import defaultdict

if len(sys.argv)>1:
    target=sys.argv[1]
    iter=int(sys.argv[2])
else:
    target = 'D'
    iter = 0

def mean(l):
    return sum(l)*1.0/len(l)

levels = { 'A':set(),'B':set(),'C':set(),'D':set(),'E':set(),'F':set(),'G':set() }
prior={}
ls_hist={}
ans={}
mfreq={}
quotes=defaultdict(int)
freq={}
last={}
llast={}
costw = {}
chist = defaultdict(list)
costdir={}
avg_co = {}
costlvl = {}
risk = {}
ca={}
tprior=defaultdict(int)
ho={}
dp={}
cp={}
mc={}
cv={}
cvm={}
gs={}
ao={}
wt={}
for col in ('A','B','C','D','E','F','G'):
    prior[col] = defaultdict(int)
    costw[col] = defaultdict(list)
    avg_co[col] = defaultdict(list)

f=open('trains1.csv','r')
h=f.readline()
for l in f:
    a=l.rstrip().split(',')
    id=a[0]
    rt=a[2]
    cs=float(a[24])
    if id not in ls_hist:
        ls_hist[id] = defaultdict(int)
        bestf = { 'A':0, 'B':0, 'C':0, 'D':0, 'E':0, 'F':0, 'G':0 }
        hist = { 'A':[-1], 'B':[-1], 'C':[-1], 'D':[-1], 'E':[-1], 'F':[-1], 'G':[-1] }
        freq[id] = {}
        mfreq[id] = {}
        last[id] = {}
        llast[id] = {}
        costdir[id] = {}
    if rt=='1':
        ans[id]={}
        costlvl[id] = mean(chist[target])
        tprior[''.join(a[17:24])]+=1
    else:
        quotes[id] += 1
        risk[id] = a[11]
    for col in ('A','B','C','D','E','F','G'):
        val = a[ord(col)-48]
        if col not in costdir[id]:
            costdir[id][col] = {}
        levels[col].add(val)
        if rt=='1':
            last_val = lasta[ord(col)-48]
            last[id][col] = last_val
            wt[id] = 1
            for col2 in ('A','B','C','D','E','F','G'):
                if col2!=target:
                    if a[ord(col2)-48]==lasta[ord(col2)-48]:
                        wt[id] += 1
            while hist[col][-1]==last_val:
                ls_hist[id][col] += 1
                hist[col].pop()
            llast[id][col] = hist[col][-1]
            ans[id][col] = val
            prior[col][last_val]+=1
            hist[col] = [-1]
            costdir[id][col]=chist[col][-1]*1.0/(mean(chist[col][:-1]))
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
            gs[id]=a[7]
            ho[id]=a[8]
            ca[id]=a[9]
            dp[id]=a[16]
            cp[id]=a[15]
            mc[id]=a[14]
            ao[id]=a[12]
            if a[10]=='':
                cv[id]=0
                cvm[id]=1
            else:
                cv[id]=ord(a[10])
                cvm[id]=0
            if col not in freq[id]:
                freq[id][col] = defaultdict(int)
            freq[id][col][val] += 1
            if freq[id][col][val] >= bestf[col]:
                bestf[col] = freq[id][col][val]
                mfreq[id][col] = val
            hist[col].append(val)
            costw[col][val].append(cs)
            chist[col].append(cs)
    lasta=a

plast={}
if iter>0:
    pred={}
    pred['A']=cPickle.load(open('predA%d.out' % (iter-1),'rb'))
    pred['B']=cPickle.load(open('predB%d.out' % (iter-1),'rb'))
    pred['C']=cPickle.load(open('predC%d.out' % (iter-1),'rb'))
    pred['D']=cPickle.load(open('predD%d.out' % (iter-1),'rb'))
    pred['E']=cPickle.load(open('predE%d.out' % (iter-1),'rb'))
    pred['F']=cPickle.load(open('predF%d.out' % (iter-1),'rb'))
    pred['G']=cPickle.load(open('predG%d.out' % (iter-1),'rb'))
    for id in last.keys():
        plast[id]={}
        plast[id]['A'] = str(pred['A'][str(int(id))][0])
        plast[id]['B'] = str(pred['B'][str(int(id))][0])
        plast[id]['C'] = str(pred['C'][str(int(id))][0])
        plast[id]['D'] = str(pred['D'][str(int(id))][0])
        plast[id]['E'] = str(pred['E'][str(int(id))][0])
        plast[id]['F'] = str(pred['F'][str(int(id))][0])
        plast[id]['G'] = str(pred['G'][str(int(id))][0])
else:
    plast=last

rd = {
    'NA': (1,0,0,0,0),
    '1': (0,1,0,0,0),
    '2': (0,0,1,0,0),
    '3': (0,0,0,1,0),
    '4': (0,0,0,0,1),
}
for i in avg_co[target].keys():
    avg_co[target][i] = mean(avg_co[target][i])
f=open('train6'+target+str(iter)+'.csv','w')
f.write("id,wt,rest,y,ls")
for lvl in sorted(list(levels[target])):
    f.write(',rel_freq_%s' % lvl)
for lvl in sorted(list(levels[target])):
    f.write(',abs_freq_%s' % lvl)
for lvl in sorted(list(levels[target])):
    f.write(',lprior_%s' % lvl)
for lvl in sorted(list(levels[target])):
    f.write(',pprior_%s' % lvl)
f.write(",ls_hist,frls,frmf,quotes,nfrls,nfrmf,frrt,prrt,csls,csmf,risk0,risk1,risk2,risk3,risk4,csdir,ca,ho,dp,cp,cv,cvm,mc,ao,gs,costlvl")
for col2 in ('A','B','C','D','E','F','G'):
    for lvl in sorted(list(levels[col2])):
        f.write(','+col2+lvl)
for col2 in ('A','B','C','D','E','F','G'):
    for lvl in sorted(list(levels[col2])):
        f.write(',pred'+col2+lvl)
f.write('\n')
for id in ans.keys():
    ls = last[id][target]
    #mf = mfreq[id][target]
    mf = llast[id][target]
    if mf==-1:
        mf = ls
    #if mf==-1 or ans[id][target] not in (ls,mf):
        #continue
    rest = 1
    for col2 in ('A','B','C','D','E','F','G'):
        if col2 != target:
            if ans[id][col2]!=plast[id][col2]:
                rest=0
    f.write("%s,%d,%d,%s,%s" % (id,wt[id],rest,ans[id][target],ls))
    for lvl in sorted(list(levels[target])):
        f.write(',%f' % (freq[id][target][lvl]*1.0/quotes[id]))
    for lvl in sorted(list(levels[target])):
        f.write(',%d' % freq[id][target][lvl])
    pll = []
    for lvl in sorted(list(levels[target])):
        pl = []
        for col2 in ('A','B','C','D','E','F','G'):
            if col2!=target:
                pl.append(last[id][col2])
            else:
                pl.append(lvl)
        pll.append(tprior[''.join(pl)]+10.0)
    for i in range(len(levels[target])):
        f.write(',%f' % (pll[i]/sum(pll)))
    pll = []
    for lvl in sorted(list(levels[target])):
        pl = []
        for col2 in ('A','B','C','D','E','F','G'):
            if col2!=target:
                pl.append(plast[id][col2])
            else:
                pl.append(lvl)
        pll.append(tprior[''.join(pl)]+10.0)
    for i in range(len(levels[target])):
        f.write(',%f' % (pll[i]/sum(pll)))
    f.write(",%d,%d,%d,%d,%f,%f,%f,%f,%f,%f" % (ls_hist[id][target],freq[id][target][ls],freq[id][target][mf],quotes[id],freq[id][target][ls]*1.0/quotes[id],freq[id][target][mf]*1.0/quotes[id],(freq[id][target][mf]+10.0)/(freq[id][target][ls]+10.0),(prior[target][mf]+10.0)/(prior[target][ls]+10.0),avg_co[target][ls],avg_co[target][mf]))
    f.write(",%s,%s,%s,%s,%s" % rd[risk[id]])
    f.write(',%f' % (costdir[id][target],))
    f.write(',%s' % ca[id])
    f.write(',%s' % ho[id])
    f.write(',%s' % dp[id])
    f.write(',%s' % cp[id])
    f.write(',%s' % cv[id])
    f.write(',%s' % cvm[id])
    f.write(',%s' % mc[id])
    f.write(',%s' % ao[id])
    f.write(',%s' % gs[id])
    f.write(',%s' % costlvl[id])
    for col2 in ('A','B','C','D','E','F','G'):
        for lvl in sorted(list(levels[col2])):
            f.write(',%d' % (int(last[id][col2]==lvl),))
    for col2 in ('A','B','C','D','E','F','G'):
        for lvl in sorted(list(levels[col2])):
            f.write(',%d' % (int(plast[id][col2]==lvl),))
    f.write('\n')
f.close()

