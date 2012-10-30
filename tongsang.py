from sanguo import Sanguo
import time
import util
import Logger

logger = Logger.getLogger()

users = [
        #'jianjianbiaoxie',
        'suidaran',
        'zilong',
        'wood',
        'yufei',
        #'nihongxiuse',
        #'vmao',
        #'wangdaiman',
        #'daofeiwang',
]

def tongsang(uname):
    retry = 10
    t = 1
    while t <= retry:
        try:
            sanguo = Sanguo()
            sanguo.login()
            data = sanguo.tongsang(uname)
            sanguo.close()
            if not data:
                raise Exception()
            logger.info('Tongsang %s succeed.'%(uname))
            return data
        except:
            time.sleep(3)
            t += 1

def main():
    suc_list = []
    fail_list = []
    for uname in users:
        res = tongsang(uname)
        if res.has_key('exception'):
            fail_list.append(uname)
        else:
            suc_list.append(uname)
        time.sleep(2)
    logger.info('tongsang suc list %s'%(unicode(suc_list)))
    if len(fail_list) > 0:
        msg = 'tongsang %s failed'%(unicode(fail_list))
        util.notify(msg)


if __name__ == '__main__':
    main()
