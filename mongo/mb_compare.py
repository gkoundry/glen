import pymongo
import sys
import re
from bson.objectid import ObjectId
import time
import pprint

TEST_MB = ["StackCV","8.6.6"]
REFERENCE_MB = ["Metablueprint","8.6.6b"]
MAX_DAYS = 30

#source_server = 'localhost'
#source_server = 'testserv002.hq.datarobot.com'
#source_server = 'testserv003.hq.datarobot.com'
source_server = 'ec2-184-73-184-26.compute-1.amazonaws.com'

source_database = 'MMApp'
source_db = pymongo.MongoClient(source_server)[source_database]
#pred = source_db['project']
pred = source_db['leaderboard']
#pred = source_db['predictions']

def mb2str(l):
    return l[0]+' v'+l[1]

ds = {}
cr = {}
mt = {}
proj = source_db['project']
for d in proj.find():
    if 'originalName' in d and 'target' in d:
        ds[str(d['_id'])]=d['originalName']
        cr[str(d['_id'])]=d['_id'].generation_time
        if 'metric' in d:
            mt[str(d['_id'])]=d['metric']

pp=pprint.PrettyPrinter(indent=4)
sc={}
sc5={}
err={}
mbbp={}
mbbpm={}
seen={}
seen5={}
#for d in pred.find({'_id':{'$gt':id}},fields=['test','pid','blueprint','metablueprint'],sort=[('_id',1)]):
for ii in (REFERENCE_MB,TEST_MB):
    if ii[0]=='StackCV':
        i=['Metablueprint','8.6.6']
        MAX_DAYS=0.5
    else:
        i=ii
    t = int(time.time()) - int(60*60*24*MAX_DAYS)
    id = ObjectId(hex(t).replace('0x','') + "0000000000000000")
    for d in pred.find({'_id':{'$gt':id},'metablueprint':i},fields=['test','pid','blueprint','metablueprint']):
        if 'blueprint' not in d or 'pid' not in d:
            continue
        dataset = str(ds.get(str(d['pid'])))
        start_time = str(d['_id'].generation_time)
        if ii[0]=='StackCV':
            mb=TEST_MB
        else:
            mb=d['metablueprint']
        mb=mb2str(mb)
        bp=re.sub("'[0-9a-z]{32}'","'xx'",str(sorted(d['blueprint'].items(),key=lambda x:x[0])))
        if str(d['pid']) not in mt:
            metric = "Gini"
        else:
            metric = mt[str(d['pid'])]
        metric='Gini'
        if 'build_error' in d:
            err[dataset+bp] = 1
            continue
        if 'test' not in d or 'Gini' not in d['test'] or len(d['test']['Gini'])<1:
            err[dataset+bp] = 1
            continue
        pdate = cr[str(d['pid'])]
        key = dataset+'\t'+mb+'\t'+bp
        if key not in seen or seen[key]>pdate:
            seen[key] = pdate
            sc[key] = (d['test'][metric][0])
        if len(d['test'][metric])>1:
            if key not in seen5 or seen5[key]>pdate:
                sc5[key] = (d['test'][metric][1])
                seen5[key] = pdate
#            else:
#                sc5.pop(key,'')
            mbbp[dataset+'\t'+bp+'\t'+metric]=1
            mbbpm[dataset+'\t'+bp+'\t'+metric+'\t'+mb]=1

#for i,j in sc5.items():
#    print '%s\t%s' % (i,j)
print "Dataset\tBlueprint\tMetric\tOld CV1\tNew CV1\tDiff CV1\tOld CV5\tNew CV5\tDiff CV5"
for db in sorted(mbbp.keys()):
    if db+'\t'+mb2str(REFERENCE_MB) not in mbbpm or db+'\t'+mb2str(TEST_MB) not in mbbpm:
        continue
    ds,bp,mt = db.split('\t')
    sys.stdout.write(db)
    key = ds+'\t'+mb2str(REFERENCE_MB)+'\t'+bp
    sc1 = sc.get(key,'-')
    key = ds+'\t'+mb2str(TEST_MB)+'\t'+bp
    sc2 = sc.get(key,'-')
    sys.stdout.write('\t%s\t%s' % (sc1,sc2))
    if sc1 not in ('-','None',None) and sc2 not in ('-','None',None):
        sys.stdout.write('\t%f' % (sc1-sc2))
    else:
        sys.stdout.write('\t-')
    key = ds+'\t'+mb2str(REFERENCE_MB)+'\t'+bp
    sc1 = sc5.get(key,'-')
    key = ds+'\t'+mb2str(TEST_MB)+'\t'+bp
    sc2 = sc5.get(key,'-')
    sys.stdout.write('\t%s\t%s' % (sc1,sc2))
    if sc1 not in ('-','None',None) and sc2 not in ('-','None',None):
        sys.stdout.write('\t%f' % (sc1-sc2))
    else:
        sys.stdout.write('\t-')
    sys.stdout.write("\n")
