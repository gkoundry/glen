source_server = 'testserv002.hq.datarobot.com'
source_database = 'MMApp'
source_db = pymongo.MongoClient(source_server)[source_database]
pred = source_db['users']
pred.insert(
    {   u'activated': 1,
        u'password': u'$pbkdf2-sha512$7474$8X4vxbiXMub8/783xnhPiQ$jEbyDHRfUMkr5EthzfL72rLk.axlahU0VHOdlGQUxnaVHECWelE5Vx/rmoyEgr3LcS5MTKpMw.oNgzbazKyCYg',
        u'roles': {   u'53530933f9ac6378db3aacf8': [u'OWNER']},
        u'username': u'glen@datarobot.com'})
