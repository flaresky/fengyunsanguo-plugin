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

class EquipInfo:
    Color_Dict = {
                '1' : '白',
                '2' : '绿',
                '3' : '蓝',
                '4' : '紫',
                '5' : '黄',
                '6' : '红',
                }
    Type_Dict = {
                '1' : '武',
                '2' : '甲',
                '3' : '马',
                '4' : '披',
                '5' : '书',
                '6' : '符',
                }
    def __init__(self):
        self.data = self.get_equip_info()
        self.eid_dict = {}
        for einfo in self.data['userEquipInfo']:
            self.eid_dict[einfo['id']] = einfo

    def get_equip_info(self):
        retry = 10
        t = 1
        while t <= retry:
            try:
                sanguo = Sanguo()
                sanguo.login()
                data = sanguo.get_equip_info()
                sanguo.close()
                if not data:
                    raise Exception()
                else:
                    return data
            except:
                time.sleep(2)
                t += 1

    def raw_print(self):
        print json.dumps(self.data, sort_keys = False, indent = 4)

    def get_equip_ids(self):
        for einfo in self.data['userEquipInfo']:
            yield einfo['id']

    def get_magic_value(self):
        return int(self.data['magic']['value'])

    def get_magic_trend(self):
        trd = int(self.data['magic']['trend'])
        if trd == 0:
            return 'Up'
        else:
            return 'Down'

    def get_upValue_by_id(self, eid):
        return self.eid_dict[eid]['upValue']

    def get_color_by_id(self, eid):
        return self.eid_dict[eid]['color']

    def get_needLevel_by_id(self, eid):
        return self.eid_dict[eid]['needLevel']

    def get_type_by_id(self, eid):
        return self.eid_dict[eid]['type']

    def get_level_by_id(self, eid):
        return self.eid_dict[eid]['userEquip']['level']

    def get_heroName_by_id(self, eid):
        return self.eid_dict[eid]['userEquip']['heroName']

    def get_currPiece_by_id(self, eid):
        return int(self.eid_dict[eid]['userEquip']['currPiece'])

    def get_maxPiece_by_id(self, eid):
        return int(self.eid_dict[eid]['userEquip']['maxPiece'])

    def get_effectValue_by_id(self, eid):
        return self.eid_dict[eid]['userEquip']['effectValue']

    def isCoolDown(self):
        return self.data['userTime']['flag'] == '1'

    def format_print(self):
        print 'Current Magic: %d%% %s'%(self.get_magic_value(), self.get_magic_trend())
        ut = int(self.data['userTime']['time'])
        st = int(self.data['serverTime'])
        print 'User Time: %d'%(ut)
        print 'Server Time: %d'%(st)
        if ut > 0:
            print 'CD: %d seconds'%(ut-st)
            print 'CoolDown: %s'%('True' if self.isCoolDown() else 'False')

if __name__ == '__main__':
    gi = EquipInfo()
    gi.format_print()
    #gi.raw_print()
