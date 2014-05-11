import pymongo
from collections import defaultdict
import sys
from bson.objectid import ObjectId
import time
import pprint

source_server = 'ec2-184-73-184-26.compute-1.amazonaws.com'

source_database = 'MMApp'
source_db = pymongo.MongoClient(source_server)[source_database]
pred = source_db['leaderboard']

ds = {}
cr = {}
metric = {}
proj = source_db['project']
for d in proj.find():
    if 'originalName' in d and 'target' in d:
        ds[str(d['_id'])]=d['originalName']
        cr[str(d['_id'])]=d['_id'].generation_time
        if 'metric' in d:
            metric[str(d['originalName'])]=d['metric']

best_bp = {}
best_dt = {}
first_bp = {}
last_bp = {}
last_sc = {}
mdir = {
    'Gini':1,
    'AUC':1,
    'RMSE':-1,
    'RMSLE':-1,
    'Gamma Deviance':-1,
    'Gamma':-1,
    'Tweedie':-1,
    'Poisson':-1,
    'LogLoss':-1,
}
best_score = defaultdict(float)
for d in pred.find({'test':{'$exists':True}},fields=['test','pid','blueprint']):
    dset = ds.get(str(d['pid']))
    dt = str(d['_id'].generation_time).split()[0]
    if dset:
        bp = str(sorted(d['blueprint'].items(),key=lambda x:x[0]))
        if 'STK' not in bp and 'AVGBL' not in bp:
            if dset not in metric:
                metric[dset] = 'Gini'
            md = mdir[metric[dset]]
            if 'test' in d and metric[dset] in d['test'] and len(d['test'][metric[dset]])>1:
                sc = d['test'][metric[dset]][1]
                if dset not in best_score or md * sc > best_score[dset]:
                    best_score[dset] = md * sc
                    best_bp[dset] = bp
                    best_dt[dset] = dt
                if md * sc == best_score[dset] and dset in best_dt and dt > best_dt[dset]:
                    best_score[dset] = md * sc
                    best_bp[dset] = bp
                    best_dt[dset] = dt
                if dset not in first_bp or dt < first_bp[dset]:
                    first_bp[dset] = dt
                if dset not in last_bp or dt > last_bp[dset]:
                    last_bp[dset] = dt
                    last_sc[dset] = md * sc
for dset in best_bp.keys():
    print dset+'\t'+first_bp[dset]+'\t'+best_dt[dset]+'\t'+last_bp[dset]+'\t'+metric[dset]+'\t'+str(md*best_score[dset])+'\t'+str(md*last_sc[dset])+'\t'+str(best_bp[dset])

