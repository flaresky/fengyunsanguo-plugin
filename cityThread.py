
import threading
from sanguo import Sanguo
from EmailSender import EmailSender
import time
import Logger
import argparse
import datetime
import util
import sys
import json

logger = Logger.getLogger()

Sleep_Time = 60 # minutes
City_Id = 'xinye'
Zone_Id = '5'
uid_dict = {}

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
        first_time = True
        logger.info('CityThread start, cityid=%s, zoneid=%s'%(City_Id, Zone_Id))
        while True:
            city_info = self.get_city_info(City_Id, Zone_Id)
            users = city_info['users']
            logger.info('Get %d users'%(len(users)))
            if not first_time:
                # check new user
                for user in users:
                    userId = user['userId']
                    userName = user['userName']
                    level = user['level']
                    if not uid_dict.has_key(userId):
                        msg = 'Found new user name=%s level=%s'%(userName, level)
                        logger.info(msg)
                        es = EmailSender()
                        es.send_mail(msg, '')
                        es.close()
            else:
                first_time = False
            for user in users:
                userId = user['userId']
                uid_dict[userId] = user
            logger.info('CityThread will sleep %d seconds'%(Sleep_Time))
            time.sleep(Sleep_Time)

def parsearg():
    global Sleep_Time, City_Id, Zone_Id
    parser = argparse.ArgumentParser(description='upgrade keji')
    parser.add_argument('-s', '--sleep', required=False, type=int, default=14, help='the time will sleep in each round, in minutes')
    parser.add_argument('-c', '--cityid', required=False, type=str, default='xinye', help='city name')
    parser.add_argument('-z', '--zoneid', required=False, type=str, default='5', help='zone id')
    res = parser.parse_args()
    Sleep_Time = res.sleep * 60
    City_Id = res.cityid
    Zone_Id = res.zoneid
            
if __name__ == '__main__':
    parsearg()
    thread = CityThread()
    thread.start()
