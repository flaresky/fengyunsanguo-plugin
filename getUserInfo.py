#!/usr/bin/python
#encoding: utf-8
from sanguo import Sanguo
import time
import Logger
import argparse
import datetime
import util
import sys
import json

country_dict = {
    '1' : u'吴国',
    '2' : u'魏国',
    '3' : u'蜀国',
    }

def get_user(uid):
    retry = 10
    t = 1
    while t <= retry:
        try:
            sanguo = Sanguo()
            sanguo.login()
            data = sanguo.getUserInfo(uid)
            sanguo.close()
            if not data:
                raise Exception()
            else:
                return data
        except:
            time.sleep(2)
            t += 1

if len(sys.argv) > 1:
    uid = sys.argv[1]
else:
    # my id
    uid = '67201307'
uinfo = get_user(uid)
#print json.dumps(uinfo, sort_keys = False, indent = 4)
print 'Get User Info %s'%(uid)
print '\tName: %s'%(uinfo['userName'])
print '\tLevel: %s'%(uinfo['level'])
print '\tCountry: %s'%(country_dict[uinfo['countryId']])
#linfo = get_user(uinfo['laird']['id'])
#print '\tLaird: UID=%s Level=%s Name=%s'%(linfo['userId'], linfo['level'], linfo['userName'])
try:
    print ('\tLaird:  UID=%s Name=%s'%(uinfo['laird']['id'], uinfo['laird']['name'])).decode('utf-8')
except:
    print u'\tLaird: 还没人征服，赶快抢啊！！！！！！！！！'
print '\tSubjects:'
#for sid in uinfo['subjects']:
#    sinfo = get_user(sid['id'])
#    print '\t\tUID=%s Level=%s Name=%s'%(sinfo['userId'], sinfo['level'], sinfo['userName'])
for sid in uinfo['subjects']:
    print ('\t\tUID=%s Name=%s'%(sid['id'], sid['name'])).decode('utf-8')
