#!/usr/bin/python
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
from GeneralInfo import GeneralInfo
import urllib2
import json

logger = Logger.getLogger()

Passport = None
Password = None

def parsearg():
    global Passport, Password
    parser = argparse.ArgumentParser(description='Get login data')
    parser.add_argument('-u', '--user', required=True, type=str, help='user name')
    parser.add_argument('-p', '--password', required=True, type=str, help='password')
    res = parser.parse_args()
    Passport = res.user
    Password = res.password

def get_userid():
    url = 'http://mc.fysg.koramgame.com/?act=User.getInfo&passport=%s&password=%s&deviceID=000000000000000'%(Passport, Password)
    uf = urllib2.urlopen(url)
    data = uf.read()
    data = json.loads(data)
    userId = data['userId']
    return userId

def print_res(res):
    #print res
    out = ''
    for c in res:
        os = hex(ord(c))[2:]
        if len(os) < 2:
            os = '0' + os
        out = out + r'\x' + os
    print out

def main():
    parsearg()
    userId = get_userid()
    login_json = '{"KL_PASSWORD":"%s","KL_PASSPORT":"%s"}'%(Password, Passport)
    #print login_json
    ret = '\x00\x05\x00\x03\x6e\x69\x6c\x00' + chr(len(str(userId))) + str(userId) + '\x00\x01\x30\x00\x00\x00' + chr(len(login_json)) + login_json
    ret = '\x00' + chr(len(ret)) + ret

    print_res(ret)

if __name__ == '__main__':
    main()
