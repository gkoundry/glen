import pymongo
import sys
from bson.objectid import ObjectId
import time
import pprint


#source_server = 'localhost'
#source_server = 'testserv002.hq.datarobot.com'
#source_server = 'testserv003.hq.datarobot.com'
source_server = 'ec2-184-73-184-26.compute-1.amazonaws.com'

source_database = 'MMApp'
source_db = pymongo.MongoClient(source_server)[source_database]
#pred = source_db['project']
pred = source_db['leaderboard']
#pred = source_db['predictions']

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

t = int(time.time()) - int(60*60*24*0.2)
id = ObjectId(hex(t).replace('0x','') + "0000000000000000")
pp=pprint.PrettyPrinter(indent=4)
print "Dataset\tBlueprint\tOld CV1\tNew CV1\tOld CV5\tNew CV5"
sc={}
sc5={}
mbbp={}
for d in pred.find({'_id':{'$gt':id}},fields=['test','pid','blueprint','metablueprint'],sort=[('_id',1)]):
    if 'blueprint' not in d or 'pid' not in d:
        continue
    dataset = str(ds.get(str(d['pid'])))+'\t'+str(d['_id'].generation_time)
    ds1 = str(ds.get(str(d['pid'])))
    if str(d['pid']) not in mt:
        metric = "Gini"
    else:
        metric = mt[str(d['pid'])]
    if metric!='Gamma Deviance':
        continue
    bp=str(sorted(d['blueprint'].items(),key=lambda x:x[0]))
    if 'build_error' in d:
        #print dataset+'\t'+str(d['build_error'])
        continue
    if 'test' not in d or 'Gini' not in d['test'] or len(d['test']['Gini'])<1:
        #print dataset+'\tCV1'
        continue
    mb=d['metablueprint']
    mb=mb[0]+' v'+mb[1]
    sc[ds1+'\t'+mb+'\t'+bp] = (d['test'][metric][0])
    if len(d['test'][metric])>1:
        sc5[ds1+'\t'+mb+'\t'+bp] = (d['test'][metric][1])
    mbbp[ds1+'\t'+bp]=1

for db in mbbp.keys():
    ds1,bp = db.split('\t')
    sys.stdout.write('%s\t%s\t' % (ds1,bp))
    if ds1+'\tMetablueprint v0.1\t'+bp in sc:
        sys.stdout.write(str(sc[ds1+'\tMetablueprint v0.1\t'+bp])+'\t')
    else:
        sys.stdout.write("-\t")
    if ds1+'\tMetablueprint v0.2\t'+bp in sc:
        sys.stdout.write(str(sc[ds1+'\tMetablueprint v0.2\t'+bp])+'\t')
    else:
        sys.stdout.write("-\t")
    if ds1+'\tMetablueprint v0.1\t'+bp in sc5:
        sys.stdout.write(str(sc5[ds1+'\tMetablueprint v0.1\t'+bp])+'\t')
    else:
        sys.stdout.write("-\t")
    if ds1+'\tMetablueprint v0.2\t'+bp in sc5:
        sys.stdout.write(str(sc5[ds1+'\tMetablueprint v0.2\t'+bp])+'\n')
    else:
        sys.stdout.write("-\n")
