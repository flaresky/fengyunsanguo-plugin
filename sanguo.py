#!/usr/bin/env python  
import re
from socket import *
from settings import *
import Logger
import zlib
import json
import time
import select
import sys
#import util
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
        data = USER_INFO[DEFAULT_USER]['LOGIN_DATA']
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
        self.login()
        logger.info('Traning hero %s for %d hours'%(hero, hour))
        mode = TRAINING_HOUR_TO_MODE[hour]
        data = '\x00\x29\x04\x4f\x00\x25\x7b\x22\x68\x65\x72\x6f\x49\x64\x22\x3a\x22'
        data = data + UID[hero]
        data = data + '\x22\x2c\x22\x6f\x70\x22\x3a\x31\x31\x30\x33\x2c\x22\x6d\x6f\x64\x65\x22\x3a'
        data = data + str(mode)
        data = data + '\x7d'
        self.tcpClientSock.send(data)
        res = self.tcpClientSock.recv(BUFSIZE)
        res = self.decode(res)
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

    def enforce_levy(self):
        #self.login()
        data = {
                'op' : 311,
            }
        data = self.compose_data(data)
        self.tcpClientSock.send(data)
        res = self.tcpClientSock.recv(BUFSIZE)
        res = self.decode(res)
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

    def getYinkuangInfo(self, city_id, zoneid):
        self.login()
        data = {
                'cityId' : str(CITY_ID[city_id]),
                'zoneId' : int(zoneid),
                'op' : 603,
            }
        data = self.compose_data(data)
        self.tcpClientSock.send(data)
        res = self.tcpClientSock.recv(BUFSIZE)
        res = self.decode(res)
        logger.info('getYinkuangInfo CITY_ID=%s zoneid=%s'%(city_id, str(zoneid)))
        return res

    def attackYinkuang(self, zoneid, position):
        self.login()
        data = {
                'zoneId' : int(zoneid),
                'position' : int(position),
                'op' : 609,
            }
        data = self.compose_data(data)
        self.tcpClientSock.send(data)
        res = self.tcpClientSock.recv(BUFSIZE)
        res = self.decode(res)
        logger.info('attackYinkuang zoneid=%s position=%s'%(str(zoneid), str(position)))
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

    def attackBoss(self):
        data = {
                'op' : 2907,
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

    def touzi(self, cityid='309', thrive=3):
        data = {
                'op' : 907,
                'cityId' : str(cityid),
                'thrive' : int(thrive),
            }
        return self.sendData(data)

    def get_jisi_info(self):
        data = {
                'op' : 2601,
            }
        return self.sendData(data)

    def jisi(self, sid=4):
        data = {
                'op' : 2603,
                'sacrificesId' : int(sid),
            }
        return self.sendData(data)

    def get_arena_reward(self):
        data = {
                'op' : 2055,
            }
        return self.sendData(data)

    def husong_suaxin(self):
        data = {
                'op' : 2703,
            }
        return self.sendData(data)

    def husong_list(self):
        data = {
                'op' : 2701,
            }
        return self.sendData(data)

    def husong(self):
        data = {
                'op' : 2705,
            }
        self.sendData(data)
        time.sleep(0.5)
        data = {
                'op' : 2713,
            }
        return self.sendData(data, False)

    def lanjie(self, convoyId):
        data = {
                'op' : 2707,
                'convoyId' : str(convoyId)
            }
        return self.sendData(data)

    def pozen_info(self, campaignid):
        data = {
                'op' : 3001,
                'campaignId' : int(campaignid)
            }
        self.login()
        data = self.compose_data(data)
        self.tcpClientSock.send(data)
        time.sleep(2)
        res = self.tcpClientSock.recv(4096)
        res = self.decode(res)
        #res = util.decode_data(res)
        return res

    def pozen(self, armyid, op=3007):
        data = {
                'op' : int(op),
                'armyId' : int(armyid)
            }
        return self.sendData(data)

    def zhuanshen(self, hero):
        data = {
                'op' : 1139,
                'heroId' : UID[hero],
            }
        return self.sendData(data)

    def bianzhen(self, keji):
        data = {
                'isPvp' : False,
                'op' : 1155,
                'formationId' : KEJI[keji],
            }
        return self.sendData(data)

    def pvp_baoming(self):
        data = {
                'op' : 3301,
            }
        return self.sendData(data)

    def sendData(self, data, login=True):
        if login:
            self.login()
        data = self.compose_data(data)
        self.tcpClientSock.send(data)
        res = self.tcpClientSock.recv(BUFSIZE)
        res = self.decode(res)
        return res

    def task_list(self, timeout=3):
        data = {
                'op' : 1329,
            }
        self.login()
        data = self.compose_data(data)
        self.tcpClientSock.send(data)
        #select.select([self.tcpClientSock], [], [], 30)
        #self.tcpClientSock.setblocking(1)
        #self.tcpClientSock.settimeout(30)
        time.sleep(timeout)
        res = self.tcpClientSock.recv(10240)
        #print 'len is '+str(len(res))+'\n'
        res = self.decode(res)
        return res

    def task_reward(self, eventId):
        data = {
                'eventId' : str(eventId),
                'op' : 1331,
            }
        return self.sendData(data)

    def test(self):
        data = {
                'op' : 1329,
            }
        return self.sendData(data, False)
        
if __name__ == '__main__':
    import time
    #print int(time.time())
    sanguo = Sanguo()
    stime = sanguo.login()
    #res = sanguo.kuangzan()
    #res = sanguo.zuanpan()
    #res = sanguo.getCityInfo('xinye', '2')
    #res = sanguo.getYinkuangInfo('xinye', 1)
    #res = sanguo.attackYinkuang(1, 16)
    #res = sanguo.zengfu('xinye', 'yingzi')
    #stime = sanguo.login()
    #res = sanguo.tongsang('jianjianbiaoxie')
    #res = sanguo.jianzhu('zuceng')
    #res = sanguo.keji('jiwen')
    #res = sanguo.getNpcInfo('huangjia80')
    #res = sanguo.soukuang('limoges')
    #res = sanguo.task_list()
    #res = sanguo.get_general_info()
    #res = sanguo.getUserInfo('64308127')
    #res = sanguo.upgradeEquip('115863', 56, 0)
    #res = sanguo.sellEquip('965347')
    #res = sanguo.tufei('guanyu')
    #res = sanguo.get_hero('zaoyun')
    #print 'magic='+str(res)
    #res = sanguo.touzi(309, 2)
    #res = sanguo.get_jisi_info()
    #res = sanguo.jisi()
    #res = sanguo.husong_suaxin()
    #res = sanguo.husong_list()
    #res = sanguo.get_arena_reward()
    #res = sanguo.husong()
    #res = sanguo.pozen_info(3)
    res = sanguo.pvp_baoming()
    #res = sanguo.zhuanshen('goujian')
    #res = sanguo.pozen(108)
    #res = sanguo.bianzhen('yanxing')
    print json.dumps(res, sort_keys = False, indent = 4)
    #print stime
    #print int(time.time())
    #data = sanguo.zudui('wan')
    #data = sanguo.getCityInfo('xinye', 5)
    sanguo.close()
    #print 'data len ' + str(len(data))
