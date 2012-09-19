#!/usr/bin/env python  
import re
from socket import *
from settings import *
import Logger
import zlib
import json
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

logger = Logger.getLogger()

BUFSIZE = 4096

def intlen_2_hexstr(i):
    a = hex(i)[2:]
    while len(a) < 4:
        a = '0' + a
    res = ''
    res += chr(int(a[:2], 16))
    res += chr(int(a[2:], 16))
    return res

class Sanguo:
    def __init__(self):
        ADDR = (HOST, PORT)
        self.tcpClientSock = socket(AF_INET, SOCK_STREAM)
        self.tcpClientSock.connect(ADDR)
    
    def __del__(self):
        self.tcpClientSock.close()

    def decode(self, data):
        if len(data) < 4:
            return None
        try:
            zflag = data[2]
            data = data[3:]
            if zflag == '\x01':
                return json.loads(zlib.decompress(data))
            else:
                return json.loads(data)
        except:
            return None

    def compose_data(self, data):
        opcode = data['op']
        data = json.dumps(data)
        data = intlen_2_hexstr(len(data)) + data
        data = intlen_2_hexstr(opcode) + data
        data = intlen_2_hexstr(len(data)) + data
        return data

    def login(self):
        ret = None
        data = '\x00\x53\x00\x05\x00\x03\x6e\x69\x6c\x00\x08\x36\x37\x32\x30\x31\x33\x30\x37\x00\x01\x30\x00\x00\x00\x3b\x7b\x22\x4b\x4c\x5f\x50\x41\x53\x53\x57\x4f\x52\x44\x22\x3a\x22\x31\x39\x38\x33\x30\x38\x30\x39\x22\x2c\x22\x4b\x4c\x5f\x50\x41\x53\x53\x50\x4f\x52\x54\x22\x3a\x22\x66\x6c\x61\x72\x65\x73\x6b\x79\x40\x31\x36\x33\x2e\x63\x6f\x6d\x22\x7d'
        self.tcpClientSock.send(data)
        res = self.tcpClientSock.recv(BUFSIZE)
        data = '\x00\x1e\x00\xc9\x00\x1a\x7b\x22\x43\x55\x52\x52\x45\x4e\x54\x5f\x56\x45\x52\x53\x49\x4f\x4e\x22\x3a\x22\x31\x2e\x33\x31\x22\x7d'
        self.tcpClientSock.send(data)
        res = self.tcpClientSock.recv(BUFSIZE)
        data = '\x00\x0e\x01\x2d\x00\x0a\x7b\x22\x6f\x70\x22\x3a\x33\x30\x31\x7d'
        self.tcpClientSock.send(data)
        res = self.tcpClientSock.recv(BUFSIZE)
        res = self.decode(res)
        try:
            #logger.info('login return serverTime: %d'%(res['serverTime']))
            return res['serverTime']
        except:
            return None
    
    def close(self):
        self.tcpClientSock.close()

    def get_general_info(self):
        self.login()
        data = '\x00\x02\x00\xc9'
        #data = '\x00\x0e\x00\xeb\x00\x0a\x7b\x22\x6f\x70\x22\x3a\x32\x33\x35\x7d\x00\x0e\x01\x2d\x00\x0a\x7b\x22\x6f\x70\x22\x3a\x33\x30\x31\x7d'
        #data = '\x00\x17\x03\xeb\x00\x13\x7b\x22\x6f\x70\x22\x3a\x31\x30\x30\x33\x2c\x22\x74\x61\x67\x22\x3a\x31\x7d'
        self.tcpClientSock.send(data)
        res = self.tcpClientSock.recv(BUFSIZE)
        res = self.decode(res)
        return res
    
    def tufei(self, hero):
        self.login()
        data = '\x00\x29\x04\x51\x00\x25\x7b\x22\x68\x65\x72\x6f\x49\x64\x22\x3a\x22'
        data = data + UID[hero]
        data = data + '\x22\x2c\x22\x6f\x70\x22\x3a\x31\x31\x30\x35\x2c\x22\x74\x79\x70\x65\x22\x3a\x30\x7d'
        self.tcpClientSock.send(data)
        res = self.tcpClientSock.recv(BUFSIZE)
        res = self.decode(res)
        logger.info('tufei %s'%(hero))
        return res
    
    def training(self, hero, hour=2):
        logger.info('Traning hero %s for %d hours'%(hero, hour))
        mode = TRAINING_HOUR_TO_MODE[hour]
        data = '\x00\x29\x04\x4f\x00\x25\x7b\x22\x68\x65\x72\x6f\x49\x64\x22\x3a\x22'
        data = data + UID[hero]
        data = data + '\x22\x2c\x22\x6f\x70\x22\x3a\x31\x31\x30\x33\x2c\x22\x6d\x6f\x64\x65\x22\x3a'
        data = data + str(mode)
        data = data + '\x7d'
        self.tcpClientSock.send(data)
        res = self.tcpClientSock.recv(BUFSIZE)
        return res
    
    def get_hero(self, hero):
        self.login()
        data = '\x00\x20\x04\x57\x00\x1c\x7b\x22\x6f\x70\x22\x3a\x31\x31\x31\x31\x2c\x22\x68\x65\x72\x6f\x49\x64\x22\x3a\x22'
        data = data + UID[hero]
        data = data + '\x22\x7d'
        self.tcpClientSock.send(data)
        res = self.tcpClientSock.recv(BUFSIZE)
        res = self.decode(res)
        return res
    
    def tax(self):
        self.login()
        data = '\x00\x0e\x01\x35\x00\x0a\x7b\x22\x6f\x70\x22\x3a\x33\x30\x39\x7d'
        self.tcpClientSock.send(data)
        res = self.tcpClientSock.recv(BUFSIZE)
        res = self.decode(res)
        logger.info('Tax one time')
        return res

    def keji(self, kid):
        self.login()
        data = '\x00\x1e\x04\x6d\x00\x1a\x7b\x22\x74\x79\x70\x65\x49\x64\x22\x3a\x22'
        data = data + KEJI[kid]
        data = data + '\x22\x2c\x22\x6f\x70\x22\x3a\x31\x31\x33\x33\x7d'
        self.tcpClientSock.send(data)
        res = self.tcpClientSock.recv(BUFSIZE)
        res = self.decode(res)
        logger.info('Upgrade keji %s'%(kid))
        return res

    def jianzhu(self, jid):
        self.login()
        data = '\x00\x1d\x01\x2f\x00\x19\x7b\x22\x74\x79\x70\x65\x49\x64\x22\x3a\x22'
        data = data + JIANZHU[jid]
        data = data + '\x22\x2c\x22\x6f\x70\x22\x3a\x33\x30\x33\x7d'
        self.tcpClientSock.send(data)
        res = self.tcpClientSock.recv(BUFSIZE)
        res = self.decode(res)
        logger.info('Upgrade jianzhu %s'%(jid))
        return res

    def attack(self, people):
        data = '\x00\x22\x02\x69\x00\x1e\x7b\x22\x75\x73\x65\x72\x49\x64\x22\x3a\x22'
        data = data + PEOPLE_ID[people]
        data = data + '\x22\x2c\x22\x6f\x70\x22\x3a\x36\x31\x37\x7d'
        self.tcpClientSock.send(data)
        res = self.tcpClientSock.recv(BUFSIZE)
        res = self.decode(res)
        logger.info('Attack %s'%(people))
        return res

    def kuangzan(self):
        self.login()
        data = '\x00\x0e\x01\xa7\x00\x0a\x7b\x22\x6f\x70\x22\x3a\x34\x32\x33\x7d'
        self.tcpClientSock.send(data)
        res = self.tcpClientSock.recv(BUFSIZE)
        res = self.decode(res)
        logger.info('Enter kuangzan')
        return res

    def soukuang(self, pid):
        self.login()
        data = {
                'farmId' : PLANTATION[pid],
                'op' : 909,
            }
        data = self.compose_data(data)
        self.tcpClientSock.send(data)
        res = self.tcpClientSock.recv(BUFSIZE)
        res = self.decode(res)
        logger.info('soukuang pid=%s'%(str(pid)))
        return res

    def salary(self):
        data = '\x00\x0e\x01\x41\x00\x0a\x7b\x22\x6f\x70\x22\x3a\x33\x32\x31\x7d'
        self.tcpClientSock.send(data)
        res = self.tcpClientSock.recv(BUFSIZE)
        logger.info('get salary today')
        return res

    def huodong(self):
        data = '\x00\x0e\x01\x41\x00\x0a\x7b\x22\x6f\x70\x22\x3a\x33\x32\x31\x7d'
        self.tcpClientSock.send(data)
        res = self.tcpClientSock.recv(BUFSIZE)
        logger.info('get huodong salary today')
        return res

    def zengfu(self, city_id, uid):
        data = '\x00\x2f\x02\x6f\x00\x2b\x7b\x22\x6f\x70\x22\x3a\x36\x32\x33\x2c\x22\x63\x69\x74\x79\x49\x64\x22\x3a'
        data = data + CITY_ID[city_id]
        data = data + '\x2c\x22\x75\x73\x65\x72\x49\x64\x22\x3a\x22'
        data = data + PEOPLE_ID[uid]
        data = data + '\x22\x7d'
        self.tcpClientSock.send(data)
        res = self.tcpClientSock.recv(BUFSIZE)
        logger.info('zengfu %s in %s'%(uid, city_id))
        return res

    def zudui(self, armyid):
        data = '\x00\x47\x01\x97\x00\x43\x7b\x22\x6f\x70\x22\x3a\x34\x30\x37\x2c\x22\x61\x75\x74\x6f\x53\x74\x61\x72\x74\x22\x3a\x31\x2c\x22\x6c\x69\x6d\x69\x74\x54\x79\x70\x65\x22\x3a\x30\x2c\x22\x6c\x69\x6d\x69\x74\x4c\x65\x76\x65\x6c\x22\x3a\x30\x2c\x22\x61\x72\x6d\x79\x49\x64\x22\x3a'
        data = data + ARMY_ID[armyid]
        data = data + '\x7d'
        self.tcpClientSock.send(data)
        res = self.tcpClientSock.recv(BUFSIZE)
        logger.info('zudui %s'%(armyid))
        return res

    def zuanpan(self):
        data = '\x00\x0e\x00\xe3\x00\x0a\x7b\x22\x6f\x70\x22\x3a\x32\x32\x37\x7d'
        self.tcpClientSock.send(data)
        res = self.tcpClientSock.recv(BUFSIZE)
        data = '\x00\x0e\x00\xe7\x00\x0a\x7b\x22\x6f\x70\x22\x3a\x32\x33\x31\x7d'
        self.tcpClientSock.send(data)
        res = self.tcpClientSock.recv(BUFSIZE)
        data = '\x00\x17\x00\xe9\x00\x13\x7b\x22\x70\x61\x67\x65\x22\x3a\x31\x2c\x22\x6f\x70\x22\x3a\x32\x33\x33\x7d'
        self.tcpClientSock.send(data)
        res = self.tcpClientSock.recv(BUFSIZE)
        res = self.decode(res)
        return res

    def getCityInfo(self, city_id, zoneid):
        self.login()
        data = {
                'cityId' : str(CITY_ID[city_id]),
                'zoneId' : int(zoneid),
                'op' : 601,
            }
        data = self.compose_data(data)
        self.tcpClientSock.send(data)
        res = self.tcpClientSock.recv(BUFSIZE)
        res = self.decode(res)
        logger.info('getCityInfo CITY_ID=%s zoneid=%s'%(city_id, str(zoneid)))
        return res

    def getUserInfo(self, uid):
        self.login()
        data = '\x00\x22\x02\x71\x00\x1e\x7b\x22\x75\x73\x65\x72\x49\x64\x22\x3a\x22'
        data = data + str(uid)
        data = data + '\x22\x2c\x22\x6f\x70\x22\x3a\x36\x32\x35\x7d'
        self.tcpClientSock.send(data)
        res = self.tcpClientSock.recv(BUFSIZE)
        res = self.decode(res)
        logger.info('getUesrInfo uid=%s'%(str(uid)))
        return res

    def get_magic(self):
        self.login()
        data = '\x00\x17\x03\xeb\x00\x13\x7b\x22\x6f\x70\x22\x3a\x31\x30\x30\x33\x2c\x22\x74\x61\x67\x22\x3a\x31\x7d'
        self.tcpClientSock.send(data)
        res = self.tcpClientSock.recv(BUFSIZE)
        res = self.decode(res)
        try:
            return int(res['magic']['value'])
        except:
            return None

    def get_equip_info(self):
        self.login()
        data = '\x00\x17\x03\xeb\x00\x13\x7b\x22\x6f\x70\x22\x3a\x31\x30\x30\x33\x2c\x22\x74\x61\x67\x22\x3a\x31\x7d'
        self.tcpClientSock.send(data)
        res = self.tcpClientSock.recv(BUFSIZE)
        res = self.decode(res)
        return res

    def get_heros(self):
        self.login()
        data = '\x00\x0f\x04\x4d\x00\x0b\x7b\x22\x6f\x70\x22\x3a\x31\x31\x30\x31\x7d'
        self.tcpClientSock.send(data)
        res = self.tcpClientSock.recv(BUFSIZE)
        res = self.decode(res)
        return res

    def get_zudui_list(self):
        self.login()
        data = '\x00\x0e\x01\xc3\x00\x0a\x7b\x22\x6f\x70\x22\x3a\x34\x35\x31\x7d'
        self.tcpClientSock.send(data)
        res = self.tcpClientSock.recv(BUFSIZE)
        res = self.decode(res)
        return res

    def getNpcInfo(self, nid):
        data = {
                'armyId' : NPC_ID[nid],
                'op' : 503,
            }
        return self.sendData(data)

    def zengzan(self, nid):
        data = {
                'armyId' : NPC_ID[nid],
                'op' : 507,
            }
        return self.sendData(data)

    def getKejiInfo(self):
        self.login()
        data = '\x00\x0f\x04\x6b\x00\x0b\x7b\x22\x6f\x70\x22\x3a\x31\x31\x33\x31\x7d'
        self.tcpClientSock.send(data)
        res = self.tcpClientSock.recv(BUFSIZE)
        res = self.decode(res)
        #logger.info('getKejiInfo')
        return res

    def upgradeEquip(self, eid, magic, buymagic=0):
        self.login()
        data = {
                'id' : eid,
                'buyMagic' : buymagic,
                'magic' : magic,
                'op' : 1001,
            }
        data = self.compose_data(data)
        self.tcpClientSock.send(data)
        res = self.tcpClientSock.recv(BUFSIZE)
        res = self.decode(res)
        logger.info('upgradeEquip eid=%s'%(str(eid)))
        return res

    def downgradeEquip(self, eid):
        self.login()
        data = {
                'id' : eid,
                'op' : 1005,
            }
        data = self.compose_data(data)
        self.tcpClientSock.send(data)
        res = self.tcpClientSock.recv(BUFSIZE)
        res = self.decode(res)
        logger.info('downgradeEquip eid=%s'%(str(eid)))
        return res

    def sellEquip(self, eid):
        self.login()
        data = {
                'id' : eid,
                'op' : 1023,
            }
        data = self.compose_data(data)
        self.tcpClientSock.send(data)
        res = self.tcpClientSock.recv(BUFSIZE)
        res = self.decode(res)
        logger.info('sellEquip eid=%s'%(str(eid)))
        return res

    def get_sucen(self):
        data = {
                'op' : 323,
            }
        return self.sendData(data)

    def tongsang(self, uid, isname=True):
        if isname:
            uid = PEOPLE_ID[uid]
        data = {
                'op' : 337,
                'toUserId' : uid,
            }
        return self.sendData(data)

    def sendData(self, data):
        self.login()
        data = self.compose_data(data)
        self.tcpClientSock.send(data)
        res = self.tcpClientSock.recv(BUFSIZE)
        res = self.decode(res)
        return res

    def test(self):
        data = {
                'op' : 501,
                'campaignId' : 13,
            }
        return self.sendData(data)
        
if __name__ == '__main__':
    import time
    #print int(time.time())
    sanguo = Sanguo()
    stime = sanguo.login()
    #res = sanguo.kuangzan()
    #res = sanguo.zuanpan()
    res = sanguo.getCityInfo('xinye', '5')
    #res = sanguo.zengfu('xinye', 'yingzi')
    #stime = sanguo.login()
    #res = sanguo.tongsang('jianjianbiaoxie')
    #res = sanguo.jianzhu('zuceng')
    #res = sanguo.keji('jiwen')
    #res = sanguo.getNpcInfo('huangjia80')
    #res = sanguo.soukuang('limoges')
    #res = sanguo.test()
    #res = sanguo.get_general_info()
    #res = sanguo.getUserInfo('64308127')
    #res = sanguo.upgradeEquip('115863', 56, 0)
    #res = sanguo.sellEquip('836243')
    #res = sanguo.tufei('guanyu')
    #res = sanguo.get_hero('zaoyun')
    #print 'magic='+str(res)
    print json.dumps(res, sort_keys = False, indent = 4)
    #print stime
    #print int(time.time())
    #data = sanguo.zudui('wan')
    #data = sanguo.getCityInfo('xinye', 5)
    sanguo.close()
    #print 'data len ' + str(len(data))
