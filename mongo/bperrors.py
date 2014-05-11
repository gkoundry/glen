import pymongo
from collections import defaultdict
import sys
from bson.objectid import ObjectId
import time
import pprint

#source_server = 'ec2-184-73-184-26.compute-1.amazonaws.com'
source_server = 'mongo-0.prod.aws.datarobot.com'

source_database = 'MMApp'
source_db = pymongo.MongoClient(source_server)[source_database]
pred = source_db['leaderboard']

ds = {}
cr = {}
mt = {}
t = int(time.time()) - int(60*60*24*2.8)
id = ObjectId(hex(t).replace('0x','') + "0000000000000000")
proj = source_db['project']
for d in proj.find({'_id':{'$gt':id}}):
    if 'originalName' in d and 'target' in d:
        ds[str(d['_id'])]=d['originalName']
        cr[str(d['_id'])]=d['_id'].generation_time
        if 'metric' in d:
            mt[str(d['_id'])]=d['metric']

cp =  defaultdict(int)
er =  defaultdict(int)
for d in pred.find({'pid':{'$exists':True}},fields=['build_error','test','pid','blueprint']):
    pid=str(d['pid'])
    dset = ds.get(pid)
    if dset:
        if 'build_error' in d or 'test' not in d or 'Gini' not in d['test'] or len(d['test']['Gini'])<1:
            er[pid] += 1
        else:
            cp[pid] += 1

for pid in ds.keys():
    print '%s\t%d\t%d' % (ds[pid],cp[pid],er[pid])
