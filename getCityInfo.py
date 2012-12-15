#!/usr/local/bin/python
import threading
from sanguo import Sanguo
import time
import Logger
import argparse
import datetime
import util
import sys
import json

logger = Logger.getLogger()

City_Id = 'xinye'
Zone_Id = '5'

class CityThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.daemon = False
    
    def get_city_info(self, cityid, zoneid):
        retry = 10
        t = 1
        while t <= retry:
            try:
                sanguo = Sanguo()
                sanguo.login()
                data = sanguo.getCityInfo(cityid, zoneid)
                sanguo.close()
                if not data:
                    logger.error('get_city_info failed')
                    raise Exception()
                else:
                    return data
            except:
                time.sleep(2)
                t += 1

    def run(self):
        city_info = self.get_city_info(City_Id, Zone_Id)
        users = city_info['users']
        print 'getCityInfo city=%s zoneid=%s'%(City_Id, Zone_Id)
        print 'Get %d Users'%(len(users))
        for user in users:
            userId = user['userId']
            userName = user['userName']
            level = user['level']
            elevel = user['enmityLevel']
            countryId = user['countryId']
            print ('\tUid=%s level=%s enmityLevel=%s country=%s Name=%s'%(userId, level, elevel, countryId, userName)).decode('utf-8')
        #print json.dumps(users, sort_keys = False, indent = 4)

def parsearg():
    global City_Id, Zone_Id
    parser = argparse.ArgumentParser(description='upgrade keji')
    parser.add_argument('-c', '--cityid', required=False, type=str, default='xinye', help='city name')
    parser.add_argument('-z', '--zoneid', required=False, type=str, default='2', help='zone id')
    res = parser.parse_args()
    City_Id = res.cityid
    Zone_Id = res.zoneid
            
if __name__ == '__main__':
    parsearg()
    thread = CityThread()
    thread.start()
