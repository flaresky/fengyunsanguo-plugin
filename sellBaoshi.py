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
from settings import *

logger = Logger.getLogger()

def sell_baoshi(bid):
    retry = 10
    t = 1
    while t <= retry:
        try:
            sanguo = Sanguo()
            sanguo.login()
            data = sanguo.sellGem(bid)
            sanguo.close()
            if not data:
                raise Exception()
            logger.info("sell baoshi %s succeed"%(str(bid)))
            return data
        except:
            #logger.error("sell baoshi %s failed"%(str(bid)))
            time.sleep(2)
            t += 1

class baoshiInfo:
    def __init__(self):
        self.local_time = None
        self.data = self.get_hero_info()
        self.hid_dict = {}
        for hinfo in self.data['userGems']:
            self.hid_dict[hinfo['id']] = hinfo

    def check_result(self, res):
        return res.has_key('userGems')

    def get_hero_info(self):
        retry = 10
        t = 1
        while t <= retry:
            try:
                sanguo = Sanguo()
                sanguo.login()
                data = sanguo.baoshi_list()
                self.local_time = int(time.time())
                sanguo.close()
                if not data:
                    raise Exception()
                if not self.check_result(data):
                    raise Exception()
                return data
            except:
                time.sleep(2)
                t += 1

    def raw_print(self):
        print json.dumps(self.data, sort_keys = False, indent = 4)

    def get_hero_ids(self):
        for hinfo in self.data['userGems']:
            yield hinfo['id']

    def get_serverTime(self):
        return self.data['serverTime']

    def get_heroid_by_id(self, hid):
        return int(self.hid_dict[hid]['holeId'])

    def get_quality_by_id(self, hid):
        return int(self.hid_dict[hid]['quality'])

def main():
    bi = baoshiInfo()
    cnt = 0
    for bid in bi.get_hero_ids():
        heroid = bi.get_heroid_by_id(bid)
        quality = bi.get_quality_by_id(bid)
        if heroid == 0 and quality < 5:
            time.sleep(2)
            sell_baoshi(bid)
            cnt += 1
    logger.info("all baoshi sold, total %d"%(cnt))

if __name__ == '__main__':
    main()
