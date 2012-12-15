#!/usr/local/bin/python
#encoding: utf-8
from sanguo import Sanguo
import time
import Logger
import argparse
import datetime
import util
import sys
import json
from settings import UID,JIANZHU
from GeneralInfo import GeneralInfo

class JianzhuInfo:
    def __init__(self):
        self.gi = GeneralInfo()
        self.jid_dict = {}
        for kinfo in self.gi.data['userBuildings']:
            self.jid_dict[kinfo['typeId']] = kinfo
        self.kname_dict = {}
        for k,v in JIANZHU.items():
            self.kname_dict[v] = k

    def raw_print(self):
        print json.dumps(self.gi.data, sort_keys = False, indent = 4)

    def get_jianzhu_ids(self):
        for hinfo in self.gi.data['userBuildings']:
            yield hinfo['typeId']

    def get_level_by_jid(self, jid):
        return int(self.jid_dict[jid]['level'])

    def format_print(self):
        #print 'Get %d jianzhus'%(len(self.jid_dict))
        for jid in self.get_jianzhu_ids():
            if self.kname_dict.has_key(jid):
                print '%s\t\tLevel: %d'%(self.kname_dict[jid], self.get_level_by_jid(jid))

if __name__ == '__main__':
    ki = JianzhuInfo()
    ki.format_print()
    #ki.raw_print()
