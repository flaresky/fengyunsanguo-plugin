#!/usr/bin/env python
# -*- coding:utf-8 -*-

import logging
import logging.handlers
import os

import settings

mylogger = None
def getLogger(*args, **kargs):
    global mylogger
    if not mylogger:
        mylogger = logging.getLogger(*args, **kargs)
        # create folder if not exists
        if not os.path.exists(os.path.dirname(settings.LOGFILE)):
            os.makedirs(os.path.dirname(settings.LOGFILE))
        handler = logging.handlers.RotatingFileHandler(settings.LOGFILE,
                                                       maxBytes = 1048576000,
                                                       backupCount=0)
        formater = logging.Formatter(settings.LOGFORMAT)
        mylogger.setLevel(logging.DEBUG)
        handler.setFormatter(formater)
        mylogger.addHandler(handler)
        #mylogger.info("Logger Initialized")
    return mylogger

if __name__ == "__main__":
    getLogger().info("test log")
