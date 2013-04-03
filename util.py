#from PyWapFetion import *
import datetime
import time
from sanguo import Sanguo
from EmailSender import EmailSender
import Logger
import traceback
import json
import zlib

from settings import *

logger = Logger.getLogger()

def next_time(delay_sec):
    stime = datetime.datetime.today() + datetime.timedelta(seconds=delay_sec)
    return stime.strftime('%m-%d %H:%M:%S')

def format_time(sec):
    if int(sec) == 0:
        return '0'
    try:
        dt = datetime.datetime.fromtimestamp(float(sec))
        return dt.strftime('%m-%d %H:%M:%S')
    except:
        return str(sec)

def get_next_refresh_time(Server_Time):
    Server_Time = int(Server_Time)
    last_time = datetime.datetime.fromtimestamp(Server_Time)
    zero_time = last_time.replace(hour=0, minute=0, second=0)
    off_seconds = int(Server_Time) - int(time.mktime(zero_time.timetuple()))
    # 5:00
    if off_seconds < 18000:
        res = zero_time.replace(hour=5)
    # 8:30
    elif off_seconds < 30600:
        res = zero_time.replace(hour=8, minute=30)
    # 12:30
    elif off_seconds < 45000:
        res = zero_time.replace(hour=12, minute=30)
    # 15:00
    elif off_seconds < 54000:
        res = zero_time.replace(hour=15)
    # 17:00
    elif off_seconds < 61200:
        res = zero_time.replace(hour=17)
    # 19:00
    elif off_seconds < 68400:
        res = zero_time.replace(hour=19)
    # 21:00
    elif off_seconds < 75600:
        res = zero_time.replace(hour=21)
    # 21:30
    elif off_seconds < 77400:
        res = zero_time.replace(hour=21, minute=30)
    else:
        res = zero_time.replace(hour=5)
        res = res + datetime.timedelta(days=1)
    return int(time.mktime(res.timetuple())) 

def notify(msg):
    msg = USER_INFO[DEFAULT_USER]['USERNAME'] + ' --- ' + msg
    es = EmailSender()
    es.send_mail(msg, '')
    logger.info('Send an email: "%s"'%(msg))
    es.close()

    #myfetion = Fetion('13706818677','nihaoma0809')
    #myfetion.send2self(msg)
    #logger.info('Send a fetion: "%s"'%(msg))

def server_time_to_sec(st):
    st = st.split(':')
    h = 0
    m = 0
    s = 0
    if len(st) == 1:
        h = int(st[0])
    elif len(st) == 2:
        h = int(st[0])
        m = int(st[1])
    elif len(st) == 3:
        h = int(st[0])
        m = int(st[1])
        s = int(st[2])
    t = datetime.datetime.today()
    if t.hour > h:
        t = t + datetime.timedelta(days=1)
    rt = datetime.datetime(
                            year = t.year,
                            month = t.month,
                            day = t.day,
                            hour = h,
                            minute = m,
                            second = s,
    )
    return int(time.mktime(rt.timetuple()))

def get_user(uid):
    retry = 10
    t = 1
    while t <= retry:
        try:
            sanguo = Sanguo()
            sanguo.login()
            data = sanguo.getUserInfo(uid)
            sanguo.close()
            if not data:
                raise Exception()
            if not data.has_key('protectTime'):
                raise Exception('No protectTime')
            return data
        except:
            time.sleep(2 * t)
            t += 1

def sync_time():
    retry = 10
    t = 1
    while t <= retry:
        try:
            sanguo = Sanguo()
            stime = sanguo.login()
            if not stime:
                raise Exception()
            ltime = int(time.time())
            sanguo.close()
            Server_Time = stime
            Local_Server_Diff = ltime - stime
            return (Server_Time, Local_Server_Diff)
        except:
            time.sleep(2)
            t += 1

def get_sleep_time(do_server_time, local_server_diff):
    return int(do_server_time) + int(local_server_diff) - int(time.time()) + 1

def intlen_2_hexstr(i):
    a = hex(i)[2:]
    while len(a) < 4:
        a = '0' + a
    res = ''
    res += chr(int(a[:2], 16))
    res += chr(int(a[2:], 16))
    return res

def check_heroes(hlist):
    for hero in hlist:
        if not UID.has_key(hero):
            return False
    return True

def check_jianzhu(jlist):
    for jid in jlist:
        if not JIANZHU.has_key(jid):
            return False
    return True

def check_keji(klist):
    for kid in klist:
        if not KEJI.has_key(kid):
            return False
    return True

def check_peoples(plist):
    for pid in plist:
        if not PEOPLE_ID.has_key(pid):
            return False
    return True

def check_plantation(plist):
    for pid in plist:
        if not PLANTATION.has_key(pid):
            return False
    return True

def check_armys(alist):
    for aid in alist:
        if not ARMY_ID.has_key(aid):
            return False
    return True


def send_data(dicdata, check_key=None):
    retry = 10
    t = 1
    while t <= retry:
        try:
            sanguo = Sanguo()
            sanguo.login()
            sanguo.login()
            data = sanguo.compose_data(dicdata)
            sanguo.tcpClientSock.send(data)
            res = sanguo.tcpClientSock.recv(4096)
            data = sanguo.decode(res)
            if check_key:
                if not data.has_key(check_key):
                    raise Exception()
            sanguo.close()
            if not data:
                raise Exception()
            return data
        except:
            #logger.error(traceback.format_exc())
            time.sleep(2)
            t += 1

def decode_data(dl):
    def decode(data):
        zflag = data[0]
        data = data[1:]
        if zflag == '\x01':
            data = zlib.decompress(data)
        return json.loads(data)

    ret = []
    idx = 0
    while idx < len(dl):
        #slen = dl[idx] + dl[idx+1]
        length = 256 * ord(dl[idx]) + ord(dl[idx+1])
        if length > 0:
            data = dl[idx+2:idx+length+2]
            res = decode(data)
            ret.append(res)
        idx += length + 2
    return ret

if __name__ == '__main__':
    #notify('magic is 22%')
    #print intlen_2_hexstr(15)
    #t1 = time.time()
    #t1 = datetime.datetime.today().replace(hour=20)
    #t1 = int(time.mktime(t1.timetuple()))
    #print 't1: ' + str(datetime.datetime.fromtimestamp(t1))
    #t2 = get_next_refresh_time(t1)
    #print 't2: ' + str(datetime.datetime.fromtimestamp(t2))
    #data = {
    #        'op' : 1323,
            #'level' : '1',
            #'type' : '3',
    #    }
    #res = send_data(data)
    #res = get_user('66702307')
    res = get_user('67201307')
    print json.dumps(res, sort_keys = False, indent = 4)
