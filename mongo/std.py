import pymongo
import sys
from bson.objectid import ObjectId
import time
import pprint


#source_server = 'localhost'
source_server = 'testserv002.hq.datarobot.com'
#source_server = 'testserv003.hq.datarobot.com'
#source_server = 'ec2-184-73-184-26.compute-1.amazonaws.com'

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

t = int(time.time()) - int(60*60*24*12.8)
id = ObjectId(hex(t).replace('0x','') + "0000000000000000")
pp=pprint.PrettyPrinter(indent=4)
ranks={}
dsm={}
mto={
    'RMSLE': 1,
    'RMSE': 1,
    'LogLoss': 1,
    'Poisson Deviance': 1,
    'Tweedie Deviance': 1,
    'AUC': -1,
    'GiniNorm': -1,
}
print "Dataset\tDate\tMetric\tScore\tBlueprint"
scl={}
for d in pred.find({'_id':{'$gt':id}},fields=['build_error','test','pid','blueprint','metablueprint'],sort=[('_id',1)]):
    if 'blueprint' not in d:
        continue
    if 'pid' in d:
        dataset = str(ds.get(str(d['pid'])))+'\t'+str(d['_id'].generation_time)
        ds1 = str(ds.get(str(d['pid'])))
        if str(d['pid']) not in mt:
            metric = "Gini"
        else:
            metric = mt[str(d['pid'])]
    else:
        dataset = '??? '+str(d['_id'].generation_time)
        metric = "Gini"
    bp=str(sorted(d['blueprint'].items(),key=lambda x:x[0]))
    if 'build_error' in d:
        #print dataset+'\t'+str(d['build_error'])
        continue
    if 'test' not in d or 'Gini' not in d['test'] or len(d['test']['Gini'])<2:
        #print dataset+'\tCV1'
        continue
    d1,t1 = dataset.split('\t')
    scl['%s\t%s\t%s' % (d1,metric,bp)] = d['test'][metric][1]
    #print '%s\t%s\t%f\t%s' % (dataset,metric,d['test'][metric][1],bp)

source_server = 'ec2-184-73-184-26.compute-1.amazonaws.com'

source_database = 'MMApp'
source_db = pymongo.MongoClient(source_server)[source_database]
#pred = source_db['project']
pred = source_db['leaderboard']
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

t = int(time.time()) - int(60*60*24*32.8)
id = ObjectId(hex(t).replace('0x','') + "0000000000000000")
print "Dataset\tDate\tMetric\tScore\tBlueprint"
seen={}
for d in pred.find({'_id':{'$gt':id}},fields=['build_error','test','pid','blueprint'],sort=[('_id',1)]):
    if 'blueprint' not in d:
        continue
    if 'pid' in d:
        dataset = str(ds.get(str(d['pid'])))+'\t'+str(d['_id'].generation_time)
        ds1 = str(ds.get(str(d['pid'])))
    else:
        dataset = '??? '+str(d['_id'].generation_time)
    if 'pid' not in d or str(d['pid']) not in mt:
        metric = "Gini"
    else:
        metric = mt[str(d['pid'])]
    bp=str(sorted(d['blueprint'].items(),key=lambda x:x[0]))
    if 'build_error' in d:
        #print dataset+'\t'+str(d['build_error'])
        continue
    if 'test' not in d or 'Gini' not in d['test'] or len(d['test']['Gini'])<2:
        #print dataset+'\tCV1'
        continue
    #print '%s\t%s\t%f\t%s' % (dataset,metric,d['test'][metric][1],bp)
    d1,t1 = dataset.split('\t')
    if '%s\t%s\t%s' % (d1,metric,bp) in scl and "'ST" in bp and 'STK' not in bp and d1+metric+bp not in seen:
        seen[d1+metric+bp]=1
        print '%s\t%s\t%f\t%f\t%s' % (dataset,metric,d['test'][metric][1],scl['%s\t%s\t%s' % (d1,metric,bp)],bp)
