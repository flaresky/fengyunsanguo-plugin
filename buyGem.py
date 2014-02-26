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


if __name__ == '__main__':
    while True:
        gemres = util.send_command('buyGem')
        if gemres is not None:
            try:
                id = gemres['id']
                logger.info('buy box ' + str(id))
                gemres = util.send_command('openGem', id)
                if gemres is not None:
                    items = gemres['items']
                    for item in items:
                        if item.has_key('userGemId'):
                            gemid = item['userGemId']
                            logger.info('get gem ' + str(gemid))
                            util.send_command('sellGem', gemid)
                        else:
                            num = item['num']
                            logger.info('get shuishi ' + str(num))
            except:
                logger.info('res is ' + json.dumps(gemres))
        time.sleep(2)
