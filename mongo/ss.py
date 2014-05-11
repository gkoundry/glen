import pymongo
import sys
from bson.objectid import ObjectId
import time
import pprint


#source_server = 'localhost'
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

t = int(time.time()) - int(60*60*24*0.8)
id = ObjectId(hex(t).replace('0x','') + "0000000000000000")
pp=pprint.PrettyPrinter(indent=4)
seen={}
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
ss={}
for d in pred.find({'_id':{'$gt':id}},fields=['build_error','test','pid','blueprint']):
    if 'pid' in d:
        dataset = str(ds.get(str(d['pid'])))+'\t'+str(d['_id'].generation_time)
        ds1 = str(ds.get(str(d['pid'])))
    else:
        dataset = '??? '+str(d['_id'].generation_time)
    if ds1 not in ss:
        ss[ds1]={}
    if 'test' not in d or 'Gini' not in d['test'] or len(d['test']['Gini'])<1:
        ss[ds1][str(sorted(d['blueprint'].items(),key=lambda x:x[0]))] = 999
    if 'test' not in d or 'Gini' not in d['test'] or len(d['test']['Gini'])<2:
        continue
    metric = mt[str(d['pid'])]
    if ds1+str(sorted(d['blueprint'].items(),key=lambda x:x[0])) in seen:
        continue
    bp=d['blueprint']
    if len(bp['1'][0][0])>3:
        bp['1'][0][0] = 'x'
    seen[ds1+str(sorted(d['blueprint'].items(),key=lambda x:x[0]))]=1
    if 'build_error' in d:
        ss[ds1][str(sorted(d['blueprint'].items(),key=lambda x:x[0]))] = 999
    else:
        #print '%s\t%s\t%f\t%s' % (dataset,metric,d['test'][metric][1],d['blueprint'])
        ss[ds1][str(sorted(d['blueprint'].items(),key=lambda x:x[0]))] = d['test'][metric][1]

t = int(time.time()) - int(60*60*24*0.8)
id = ObjectId(hex(t).replace('0x','') + "0000000000000000")
t = int(time.time()) - int(60*60*24*15.8)
id2 = ObjectId(hex(t).replace('0x','') + "0000000000000000")
pp=pprint.PrettyPrinter(indent=4)
seen={}
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
ns={}
mtd={}
for d in pred.find({'_id':{'$gt':id2,'$lt':id}},fields=['build_error','test','pid','blueprint']):
    if 'pid' in d:
        dataset = str(ds.get(str(d['pid'])))+'\t'+str(d['_id'].generation_time)
        ds1 = str(ds.get(str(d['pid'])))
    else:
        dataset = '??? '+str(d['_id'].generation_time)
    if ds1 not in ns:
        ns[ds1]={}
    if 'test' not in d or 'Gini' not in d['test'] or len(d['test']['Gini'])<1:
        ns[ds1][str(sorted(d['blueprint'].items(),key=lambda x:x[0]))] = 999
    if 'test' not in d or 'Gini' not in d['test'] or len(d['test']['Gini'])<2:
        continue
    metric = mt[str(d['pid'])]
    if ds1+str(sorted(d['blueprint'].items(),key=lambda x:x[0])) in seen:
        continue
    bp=d['blueprint']
    if len(bp['1'][0][0])>3:
        bp['1'][0][0] = 'x'
    mtd[ds1]=metric
    if ds1 in ss:
        seen[ds1+str(sorted(d['blueprint'].items(),key=lambda x:x[0]))]=1
        if ds1 not in ns:
            ns[ds1]={}
        if 'build_error' in d:
            ns[ds1][str(sorted(d['blueprint'].items(),key=lambda x:x[0]))] = 999
        else:
            #print '%s\t%s\t%f\t%s' % (dataset,metric,d['test'][metric][1],d['blueprint'])
            ns[ds1][str(sorted(d['blueprint'].items(),key=lambda x:x[0]))] = d['test'][metric][1]

for ds in ss.keys():
    if ds in ns:
        for bp in ss[ds].keys():
            if bp in ns[ds]:
                print '%s\t%s\t%s\t%f\t%f' % (ds,bp,mtd[ds],ns[ds][bp],ss[ds][bp])
