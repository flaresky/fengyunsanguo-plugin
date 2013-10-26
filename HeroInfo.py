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

class HeroInfo:
    def __init__(self):
        self.local_time = None
        self.data = self.get_hero_info()
        self.hid_dict = {}
        for hinfo in self.data['heros']:
            self.hid_dict[hinfo['id']] = hinfo

    def check_result(self, res):
        return res.has_key('heros')

    def get_hero_info(self):
        retry = 10
        t = 1
        while t <= retry:
            try:
                sanguo = Sanguo()
                sanguo.login()
                data = sanguo.get_heros()
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
        for hinfo in self.data['heros']:
            yield hinfo['id']

    def get_serverTime(self):
        return self.data['serverTime']

    def get_exp_speed_by_id(self, hid):
        return int(self.hid_dict[hid]['expSpeed'])

    def get_exp_speed(self):
        res = 100000000000
        for hid in self.get_hero_ids():
            tpep = self.get_exp_speed_by_id(hid)
            if tpep > 0:
                res = min(res, tpep)
        return res

    def get_name_by_id(self, hid):
        return self.hid_dict[hid]['name']

    def get_level_by_id(self, hid):
        return self.hid_dict[hid]['level']

    def get_grade_by_id(self, hid):
        return self.hid_dict[hid]['grade']

    def get_leadership_by_id(self, hid):
        return self.hid_dict[hid]['leadership']

    def get_tactics_by_id(self, hid):
        return self.hid_dict[hid]['tactics']

    def get_currUnit_by_id(self, hid):
        return self.hid_dict[hid]['currUnit']

    def get_magic_by_id(self, hid):
        return self.hid_dict[hid]['magic']

    def get_nextrebirthlevel_by_id(self, hid):
        return self.hid_dict[hid]['nextRebirthLevel']

    def get_trainingEndTime_by_id(self, hid):
        return self.hid_dict[hid]['trainingEndTime']

    def get_maxLevel_by_id(self, hid):
        return int(self.hid_dict[hid]['maxLevel'])

    def get_nextUpgrade_by_id(self, hid):
        return self.hid_dict[hid]['nextUpgrade']

    def get_exp_id(self, hid):
        return float(self.hid_dict[hid]['exp'])

    def get_lastModify_id(self, hid):
        return int(self.hid_dict[hid]['lastModify'])

    def calc_cur_exp_by_id(self, hid):
        exp = self.get_exp_id(hid)
        if exp <= 0:
            return 0
        t = self.get_serverTime() - self.get_lastModify_id(hid)
        exp += float(t) * self.get_exp_speed_by_id(hid) / 3600
        return int(exp)

    def format_print(self):
        print 'Get %d heros'%(len(self.hid_dict))
        for hid in self.get_hero_ids():
            cur_exp = self.calc_cur_exp_by_id(hid)
            print 'Hero: %s'%(self.get_name_by_id(hid))
            print '\tID: %s'%(hid)
            print '\tLevel: %s\tGrade: %s'%(self.get_level_by_id(hid), self.get_grade_by_id(hid))
            if cur_exp > 0:
                print '\tExp: %d/%d'%(self.calc_cur_exp_by_id(hid), LEVEL_EXP_MAP.get(int(self.get_level_by_id(hid)), 0))
            print '\tArmy: %s'%(self.get_currUnit_by_id(hid))
            print '\t统:%s\t勇:%s\t智:%s'%(self.get_leadership_by_id(hid), self.get_tactics_by_id(hid), self.get_magic_by_id(hid))
            print '\tNextRebirthLevel: %s'%(self.get_nextrebirthlevel_by_id(hid))
            if self.get_trainingEndTime_by_id(hid) <> '0':
                print '\tTrainingEndTime: %s'%(util.format_time(self.get_trainingEndTime_by_id(hid)))
            if self.get_nextUpgrade_by_id(hid) <> '0':
                print '\tNextUpgrade: %s'%(util.format_time(self.get_nextUpgrade_by_id(hid)))

    def print_for_setting(self):
        for hid in self.get_hero_ids():
            print "'%s' : '%s',"%(self.get_name_by_id(hid), str(hid))

if __name__ == '__main__':
    hi = HeroInfo()
    hi.format_print()
    #hi.raw_print()
    hi.raw_print()
    hi.print_for_setting()
