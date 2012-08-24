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
                '1' : u'白',
                '2' : u'绿',
                '3' : u'蓝',
                '4' : u'紫',
                '5' : u'黄',
                '6' : u'红',
                }
    Type_Dict = {
                '1' : u'武',
                '2' : u'甲',
                '3' : u'马',
                '4' : u'披',
                '5' : u'书',
                '6' : u'符',
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
                if not data.has_key('userEquipInfo'):
                    raise Exception()
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

    def get_magic_needgold(self):
        return int(self.data['magic']['magicNeedGold'])

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

    def get_needCoin_by_id(self, eid):
        return self.eid_dict[eid]['needCoin']

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
        print 'MagicNeedGold: %d'%(self.get_magic_needgold())
        if ut > 0:
            print 'CD: %d seconds'%(ut-st)
            print 'CoolDown: %s'%('True' if self.isCoolDown() else 'False')
        print 'Equips Info:'
        for eid in self.get_equip_ids():
            print '\tEID %s'%(eid)
            print '\t\tType: %s级%s%s +%s'%(
                                        self.get_needLevel_by_id(eid),
                                        self.Color_Dict[self.get_color_by_id(eid)],
                                        self.Type_Dict[self.get_type_by_id(eid)],
                                        self.get_upValue_by_id(eid),
                                        )
            print '\t\tLevel: %s'%(self.get_level_by_id(eid))
            print '\t\tValue: %s'%(self.get_effectValue_by_id(eid))
            print '\t\tNeedCoin: %s'%(self.get_needCoin_by_id(eid))
            if self.get_heroName_by_id(eid):
                print '\t\tHero: %s'%(self.get_heroName_by_id(eid))
            if self.get_currPiece_by_id(eid) < self.get_maxPiece_by_id(eid):
                print '\t\tPieces: %d/%d'%(self.get_currPiece_by_id(eid), self.get_maxPiece_by_id(eid))

if __name__ == '__main__':
    gi = EquipInfo()
    gi.format_print()
    #gi.raw_print()
