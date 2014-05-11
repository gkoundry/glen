import pymongo
from bson.objectid import ObjectId
import time
import pprint

#
# Remove predictions more than a week old
#

#source_server = 'mongo-0.prod.aws.datarobot.com'
#source_server = 'localhost'
source_server = 'testserv002.hq.datarobot.com'
#source_server = 'testserv003.hq.datarobot.com'
#source_server = 'ec2-184-73-184-26.compute-1.amazonaws.com'

source_database = 'MMApp'
source_db = pymongo.MongoClient(source_server)[source_database]
#pred = source_db['project']
#pred = source_db['model_code']
#pred = source_db['users']
#pred = source_db['eda']
#pred = source_db['eda_map']
pred = source_db['leaderboard']
#pred = source_db['predictions']
#pred = source_db['metadata']

ds = {}
cr = {}
proj = source_db['project']
for d in proj.find():
    if 'originalName' in d and 'target' in d:
        ds[str(d['_id'])]=d['originalName']
        cr[str(d['_id'])]=d['_id'].generation_time

t = int(time.time()) - int(60*60*24*7.5)
id = ObjectId(hex(t).replace('0x','') + "0000000000000000")
pp=pprint.PrettyPrinter(indent=4)
for d in pred.find({'_id':{'$gt':id}}):
#for d in pred.find({'_id':{'$gt':id}},fields=['pid','blueprint','test','build_error','samplepct']):
#for d in pred.find({'pid':ObjectId('5347b168fca41d6319da2963')}):
    if 'pid' not in d or str(d['pid']) not in ds or 'MAGIC-Ga' not in ds[str(d['pid'])]:
        continue
    print str(d['_id'].generation_time)
    if 'partition_stats' in d:
        print d['blueprint']
        t=d['partition_stats']
        for rep in t.keys():
            print '%s %f' % (rep,float(t[rep]['time_real']))
        #pp.pprint(d['task_info'])

        t=d['task_info']
        for rep in t.keys():
            for v in t[rep]:
                for ts in v:
                    for k,i in ts.items():
                        if 'CPU time' in k:
                            print '%s %s %s %s %f %s' % (rep,d['samplepct'],ts['task_name'],k,i,ts['cached'])
        if 'AVGBL' in str(d['blueprint']):
            pp.pprint(d)
        print ''
