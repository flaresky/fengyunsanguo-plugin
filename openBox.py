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


if __name__ == '__main__':
    boxlist = util.send_command('getBoxList')
    if boxlist is not None:
        ids = []
        for val in boxlist['userTreasurebox'].values():
            ids.append(val['id'])
        logger.info('get box list succeed, %d boxes'%(len(ids)))
        for id in ids:
            while True:
                time.sleep(2)
                res = util.send_command('openBox', id)
                if res is not None:
                    if res.has_key('exception'):
                        logger.info('open box %s exception %s'%(str(id), res['exception']['message']))
                        break
                    else:
                        logger.info('open box %s succeed'%(str(id)))
        logger.info('all opened, exit')
