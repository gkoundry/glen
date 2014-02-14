import pymongo
import requests
import json
from requests.auth import HTTPBasicAuth

# get some collections from MB testing database
source_server = 'localhost'
source_database = 'MMApp'
source_db = pymongo.MongoClient(source_server)[source_database]
leaderboard = source_db['leaderboard']
projects = source_db['project']

print "Get current project ID"
current_project = projects.find_one(sort=[('created', -1)])
pid = current_project.get('_id')
print pid
print ""

print "Login"
s = requests.Session()
r = s.post(
    'http://localhost/account/login',
    data=json.dumps({'username': 'blah@blah.com', 'password': 'temp1234'}),
    headers={'Content-type': 'application/json', 'Accept': 'text/plain'},
    auth=HTTPBasicAuth('user', 'pass'))
print r.text
print

print "Upload file"
url = 'http://localhost/project/%s/newdata_upload' % str(pid)
#files = {'file': open('/home/glen/datasets/testdata/kickcars_test.csv', 'rb')}
files = {'file': open('/home/glen/datasets/testdata/influencers_test.csv', 'rb')}
#files = {'file': open('/home/glen/datasets/testdata/credit-train-small.csv', 'rb')}
r = s.post(url, files=files, auth=HTTPBasicAuth('user', 'pass'))
print r.text
print

print "Get best model"
best_gini = -999
lid = None
for doc in leaderboard.find({'pid': pid, 'test': {'$exists': True}}):
    if len(doc['test']['Gini']) == 2:
        if doc['test']['Gini'][1] > best_gini:
            best_gini = doc['test']['Gini']
            lid = doc['_id']

if lid:
    print str(lid)
else:
    print 'No 5-fold leaderboard items found.'
print
