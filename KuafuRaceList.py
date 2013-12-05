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

class KuafuRaceList:
    def __init__(self):
        self.local_time = None
        self.data = self.get_hero_info()
        self.hid_dict = {}
        self.hid_dict['me'] = self.data['userInfo']
        for hinfo in self.data['rankRaceUsers']:
            self.hid_dict[hinfo['centerUserId']] = hinfo

    def check_result(self, res):
        return res.has_key('rankRaceUsers')

    def get_hero_info(self):
        retry = 10
        t = 1
        while t <= retry:
            try:
                sanguo = Sanguo()
                sanguo.login()
                data = sanguo.kuafu_race_list()
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
        for hinfo in self.data['rankRaceUsers']:
            yield hinfo['centerUserId']

    def get_inspireTimes_by_id(self, hid):
        return int(self.hid_dict[hid]['inspireTimes'])

    def get_name_by_id(self, hid):
        return self.hid_dict[hid]['name']

    def get_level_by_id(self, hid):
        return self.hid_dict[hid]['level']

    def get_fightPoint_by_id(self, hid):
        return self.hid_dict[hid]['fightPoint']

    def get_rank_by_id(self, hid):
        return self.hid_dict[hid]['rank']

    def get_serverMark_by_id(self, hid):
        return self.hid_dict[hid]['serverMark']

    def get_fightPower_by_id(self, hid):
        return self.hid_dict[hid]['fightPower']

    def format_print(self):
        self.format_print_by_id('me')
        print 'Get %d users'%(len(self.hid_dict))
        for hid in self.get_hero_ids():
            self.format_print_by_id(hid)

    def format_print_by_id(self, hid):
        print '%s %s Lv%s'%(self.get_rank_by_id(hid), self.get_name_by_id(hid), self.get_level_by_id(hid))
        #print '\tLevel: %s'%(self.get_level_by_id(hid))
        print '\t战力值: %s'%(self.get_fightPower_by_id(hid))
        print '\t鼓舞次数: %s'%(self.get_inspireTimes_by_id(hid))
        print '\tserver: %s'%(self.get_serverMark_by_id(hid))
        print '\t积分: %s'%(self.get_fightPoint_by_id(hid))

    def print_for_setting(self):
        for hid in self.get_hero_ids():
            print "'%s' : '%s',"%(self.get_name_by_id(hid), str(hid))

if __name__ == '__main__':
    hi = KuafuRaceList()
    hi.format_print()
    #hi.raw_print()
