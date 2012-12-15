#!/usr/local/bin/python
#encoding: utf-8
import threading
from sanguo import Sanguo
import time
import sys 
import Logger
import argparse
import datetime
import util
import traceback
from EmailSender import EmailSender
from settings import *
from HeroInfo import HeroInfo

logger = Logger.getLogger()

Hero = None
From = None
To = None
Zuansheng = 0

def parsearg():
    global Hero, From, To, Zuansheng
    parser = argparse.ArgumentParser(description='Get training time')
    parser.add_argument('-e', '--hero', required=False, type=str, help='hero name')
    parser.add_argument('-f', '--from_level', required=False, type=int, help='from level')
    parser.add_argument('-t', '--to_level', required=False, type=int, help='to level')
    parser.add_argument('-z', '--zuansheng', required=False, type=int, default=0, help='zuansheng times')
    res = parser.parse_args()
    Hero = res.hero
    From = res.from_level
    To = res.to_level
    Zuansheng = res.zuansheng

def get_time_by_level(level):
    try:
        return LEVEL_EXP_MAP[level]
    except:
        return 0

def get_training_time():
    global Hero, From, To, Zuansheng
    total_exp = 0
    hi = HeroInfo()
    exp_speed = int(hi.get_exp_speed())
    if Zuansheng > 0:
        From = 1
        To = 51
        print 'Will sum from level %d to level %d'%(From, To)
        for l in range(From, To):
            total_exp += get_time_by_level(l)
        for z in range(Zuansheng):
            To += 10
            To = min(To, 120)
            print 'Will sum from level %d to level %d'%(From, To)
            for l in range(From, To):
                total_exp += get_time_by_level(l)
    else:
        if Hero:
            hid = UID[Hero]
            exp_speed = hi.get_exp_speed_by_id(hid)
            if not From:
                From = int(hi.get_level_by_id(hid))
            if not To:
                To = min(int(hi.get_nextrebirthlevel_by_id(hid)), hi.get_maxLevel_by_id(hid))
        print 'Will sum from level %d to level %d'%(From, To)
        for l in range(From, To):
            total_exp += get_time_by_level(l)
        total_exp -= hi.calc_cur_exp_by_id(hid)
    print 'Exp Speed: %d'%(exp_speed)
    print 'Total Exp: %d'%(total_exp)
    t = total_exp / float(exp_speed)
    if t > 24:
        d = int(t / 24)
        h = t - 24 * d
        print 'Need Time: %d Days %.1f Hours'%(d, h)
    else:
        print 'Need Time: %.1f Hours'%(t)
    
if __name__ == '__main__':
    parsearg()
    get_training_time()
