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

SEASON_MAP = {
            1 : u'春天',
            2 : u'夏天',
            3 : u'秋天',
            4 : u'冬天',
}

class GeneralInfo:
    def __init__(self):
        self.local_time = None
        self.building_dict = {}
        self.data = self.get_general_info()

    def check_result(self, res):
        return res.has_key('trainingHeroNum')

    def get_general_info(self):
        retry = 10
        t = 1
        while t <= retry:
            try:
                sanguo = Sanguo()
                sanguo.login()
                data = sanguo.get_general_info()
                self.local_time = int(time.time())
                sanguo.close()
                if not data:
                    raise Exception()
                if not self.check_result(data):
                    raise Exception()
                for binfo in data['userBuildings']:
                    self.building_dict[binfo['typeId']] = binfo
                return data
            except:
                time.sleep(2)
                t += 1

    def raw_print(self):
        print json.dumps(self.data, sort_keys = False, indent = 4)

    def get_training_hero_num(self):
        return int(self.data['trainingHeroNum'])

    def get_max_training_hero_num(self):
        return int(self.data['user']['maxTraining'])

    def get_user_name(self):
        return self.data['user']['name'].decode('utf-8')

    def get_cur_silver(self):
        return int(self.data['user']['currSilver'])

    def get_max_silver(self):
        return int(self.data['user']['maxSilver'])

    def get_repute(self):
        return int(self.data['user']['repute'])

    def get_level(self):
        return int(self.data['user']['level'])

    def get_gold_num(self):
        return int(self.data['user']['goldCoin'])

    def get_levy_remain(self):
        return int(self.data['userExtend']['levyTimesRemaining'])

    def get_levy_times(self):
        return int(self.data['userExtend']['levyTimes'])

    def get_enforce_levy_times(self):
        return int(self.data['userExtend']['enforceLevyTimes'])

    def get_freeappoint_num(self):
        return int(self.data['userExtend']['freeAppoint'])

    def get_enforce_levy_times(self):
        return int(self.data['userExtend']['enforceLevyTimes'])
    def get_jewelryPoint(self):
        return int(self.data['userExtend']['jewelryPoint'])

    def get_battleTimes(self):
        return int(self.data['userExtend']['battleTimes'])

    def get_cur_mobility(self):
        return int(self.data['user']['currMobility'])

    def get_max_mobility(self):
        return int(self.data['user']['maxMobility'])

    def get_exploit(self):
        return int(self.data['user']['exploit'])

    def get_protect_time(self):
        return int(self.data['userExtend']['protectTimes'])

    def get_turntable_time(self):
        return int(self.data['userExtend']['turntableFreeTimes'])

    def get_task_finish_num(self):
        return int(self.data['userExtend']['taskDailyFinish'])

    def get_salary_collected(self):
        return int(self.data['userExtend']['salaryCollected'])

    def get_arenaReward(self):
        return int(self.data['userExtend']['arenaReward'])

    def get_userReceiveCaravan(self):
        return int(self.data['userExtend']['userReceiveCaravan'])

    def get_serverTime(self):
        return int(self.data['serverTime'])

    def get_localTime(self):
        return self.local_time

    def get_next_CDTime(self):
        res = 13409404500
        for ut in self.data['userTimes']:
            if ut['type'] == '1':
                res = min(res, int(ut['time']))
        return res

    def get_next_keji_CDTime(self):
        res = 13409404500
        for ut in self.data['userTimes']:
            if ut['type'] == '4':
                res = min(res, int(ut['time']))
        return res

    def get_tax_CDTime(self):
        res = 13409404500
        for ut in self.data['userTimes']:
            if ut['type'] == '2':
                res = min(res, int(ut['time']))
        return res

    def get_mobility_CDTime(self):
        res = 13409404500
        for ut in self.data['userTimes']:
            if ut['type'] == '11':
                res = min(res, int(ut['time']))
        return res

    def get_tufei_CDTime(self):
        res = 13409404500
        for ut in self.data['userTimes']:
            if ut['type'] == '5':
                res = min(res, int(ut['time']))
        return res

    def get_zuangbei_CDTime(self):
        res = 13409404500
        for ut in self.data['userTimes']:
            if ut['type'] == '6':
                res = min(res, int(ut['time']))
        return res

    def get_weipai_CDTime(self):
        res = 13409404500
        for ut in self.data['userTimes']:
            if ut['type'] == '7':
                res = min(res, int(ut['time']))
        return res

    def get_touzi_CDTime(self):
        res = 13409404500
        for ut in self.data['userTimes']:
            if ut['type'] == '10':
                res = min(res, int(ut['time']))
        return res

    def get_block_CDTime(self):
        res = 13409404500
        for ut in self.data['userTimes']:
            if ut['type'] == '22':
                res = min(res, int(ut['time']))
        return res

    def get_husong_suaxin_CDTime(self):
        res = 13409404500
        for ut in self.data['userTimes']:
            if ut['type'] == '23':
                res = min(res, int(ut['time']))
        return res

    def get_xiongsou_CDTime(self):
        res = 13409404500
        for ut in self.data['userTimes']:
            if ut['type'] == '24':
                res = min(res, int(ut['time']))
        return res

    def get_jianzu_level_by_jid(self, jid):
        #return int(self.data['userBuildings'][str(jid)]['level'])
        return int(self.building_dict[str(jid)]['level'])

    def get_season(self):
        return self.data['systemVariable']['season']

    def get_magic(self):
        return self.data['systemVariable']['magic']

    def format_print(self):
        print '%s:'%(self.get_user_name())
        print '\tSeason: %s'%(SEASON_MAP[self.get_season()])
        print '\tMagic: %d'%(self.get_magic())
        print '\tLevel: %d'%(self.get_level())
        print '\tTraining Status: %d/%d'%(self.get_training_hero_num(), self.get_max_training_hero_num())
        print '\tLevy Status: %d/%d'%(self.get_levy_times(), self.get_levy_times()+self.get_levy_remain())
        print '\tEnforce Levy Times: %d, Total Times: %d'%(self.get_enforce_levy_times(), self.get_levy_times()+self.get_enforce_levy_times())
        print '\tDaily Task Status: %d/6'%(self.get_task_finish_num())
        print '\tSilver Status: %d/%d'%(self.get_cur_silver(), self.get_max_silver())
        print '\tMobility Status: %d/%d'%(self.get_cur_mobility(), self.get_max_mobility())
        print '\tBattle Times: %d'%(self.get_battleTimes())
        print '\tGoldCoin: %d'%(self.get_gold_num())
        print '\tExploit: %d'%(self.get_exploit())
        print '\tRepute: %d'%(self.get_repute())
        print '\tJewelryPoint: %d'%(self.get_jewelryPoint())
        print '\tFree Appoint Remain: %d'%(self.get_freeappoint_num())
        print '\tTurntable Remain: %d'%(self.get_turntable_time())
        print '\tSalary Remain: %d'%(1-self.get_salary_collected())
        print '\tArenaReward Remain: %d'%(1-self.get_arenaReward())
        print '\tReceiveCaravan: %d'%(self.get_userReceiveCaravan())
        print '\tServerTime: %s'%(util.format_time(self.get_serverTime()))
        print '\tNext Jianzhu CD Time: %s'%(util.format_time(self.get_next_CDTime()))
        print '\tTax CD Time: %s'%(util.format_time(self.get_tax_CDTime()))
        print '\tKeji CD Time: %s'%(util.format_time(self.get_next_keji_CDTime()))
        print '\tTufei CD Time: %s'%(util.format_time(self.get_tufei_CDTime()))
        print '\tMobility CD Time: %s'%(util.format_time(self.get_mobility_CDTime()))
        print '\tWeipai CD Time: %s'%(util.format_time(self.get_weipai_CDTime()))
        print '\tZhuangbei CD Time: %s'%(util.format_time(self.get_zuangbei_CDTime()))
        print '\tTouzi CD Time: %s'%(util.format_time(self.get_touzi_CDTime()))
        print '\tBlock CD Time: %s'%(util.format_time(self.get_block_CDTime()))
        print '\tXiongsou CD Time: %s'%(util.format_time(self.get_xiongsou_CDTime()))

if __name__ == '__main__':
    gi = GeneralInfo()
    gi.format_print()
    #gi.raw_print()
