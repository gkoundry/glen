import pymongo
import sys
from bson.objectid import ObjectId
import time
import pprint

MAX_DAYS = 30

source_server = 'localhost'
#source_server = 'testserv002.hq.datarobot.com'
#source_server = 'testserv003.hq.datarobot.com'
#source_server = 'ec2-184-73-184-26.compute-1.amazonaws.com'

source_database = 'MMApp'
source_db = pymongo.MongoClient(source_server)[source_database]

ds = {}
cr = {}
mt = {}
proj = source_db['project']
pids=[]
t = int(time.time()) - int(60*60*24*MAX_DAYS)
id = ObjectId(hex(t).replace('0x','') + "0000000000000000")
for d in proj.find({'_id':{'$gt':id}}):
    if 'originalName' in d and 'target' in d:
        pids.append(str(d['_id']))
        ds[str(d['_id'])]=d['originalName']
        cr[str(d['_id'])]=d['_id'].generation_time
        if 'metric' in d:
            mt[str(d['_id'])]=d['metric']

lb = source_db['leaderboard']
for pid in pids:
    d = lb.find_one({'pid':ObjectId(pid)},['metablueprint'])
    if d:
        print '%s %s %s %s %s' % (pid,ds[pid],d['metablueprint'],cr[pid],mt.get(pid))
