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

def sell_baowu(bid):
    retry = 10
    t = 1
    while t <= retry:
        try:
            sanguo = Sanguo()
            sanguo.login()
            data = sanguo.sell_baowu(bid)
            sanguo.close()
            if not data:
                raise Exception()
            logger.info("sell baowu %s succeed"%(str(bid)))
            return data
        except:
            #logger.error("sell baowu %s failed"%(str(bid)))
            time.sleep(2)
            t += 1

class BaowuInfo:
    def __init__(self):
        self.local_time = None
        self.data = self.get_hero_info()
        self.hid_dict = {}
        for hinfo in self.data['userJewelrys']:
            self.hid_dict[hinfo['id']] = hinfo

    def check_result(self, res):
        return res.has_key('userJewelrys')

    def get_hero_info(self):
        retry = 10
        t = 1
        while t <= retry:
            try:
                sanguo = Sanguo()
                sanguo.login()
                data = sanguo.baowu_list()
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
        for hinfo in self.data['userJewelrys']:
            yield hinfo['id']

    def get_serverTime(self):
        return self.data['serverTime']

    def get_heroid_by_id(self, hid):
        return int(self.hid_dict[hid]['heroId'])

    def get_quality_by_id(self, hid):
        return int(self.hid_dict[hid]['quality'])

if __name__ == '__main__':
    bi = BaowuInfo()
    #bi.raw_print()
    #sys.exit()
    cnt = 0
    for bid in bi.get_hero_ids():
        heroid = bi.get_heroid_by_id(bid)
        quality = bi.get_quality_by_id(bid)
        if heroid == 0 and quality < 3:
            time.sleep(2)
            sell_baowu(bid)
            cnt += 1
    logger.info("all baowu sold, total %d"%(cnt))
