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
import sellBaowu

logger = Logger.getLogger()

qiemap = {
        1 : 550,
        2 : 1375,
        3 : 3506,
        4 : 7078,
        5 : 10000,
        6 : 15000,
        7 : 20000,
    }

if __name__ == '__main__':
    total = 0
    times = 0
    while True:
        gemres = util.send_command('buyGem')
        #gemres = {'id' : 84484}
        if gemres is not None:
            if gemres.has_key('exception'):
                logger.error('Got Exception "%s"'%(gemres['exception']['message']))
                continue
            try:
                id = gemres['id']
                #logger.info('buy box ' + str(id))
                time.sleep(2)
                gemres = util.send_command('openGem', id)
                if gemres is not None:
                    if gemres.has_key('exception'):
                        logger.error('Got Exception "%s"'%(gemres['exception']['message']))
                        continue
                    items = gemres['items']
                    times += 1
                    for item in items:
                        if item.has_key('userGemId'):
                            gemid = item['userGemId']
                            gid = int(item['gemId'])
                            total += qiemap[gid % 10] - 678
                            logger.info('%d get gem %d, total earn %d'%(times, gid, total))
                            time.sleep(2)
                            util.send_command('sellGem', gemid)
                        else:
                            num = int(item['num'])
                            total += num - 678
                            logger.info('%d get shuishi %d, total earn %d'%(times, num, total))
            except:
                logger.info('res is ' + json.dumps(gemres))
        time.sleep(2)
