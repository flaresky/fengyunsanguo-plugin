from sanguo import Sanguo
import time
import Logger
from zuanpanThread import ZuanpanThread

logger = Logger.getLogger()


def pvp():
    retry = 10
    t = 1
    while t <= retry:
        try:
            sanguo = Sanguo()
            sanguo.login()
            data = sanguo.pvp_baoming()
            sanguo.close()
            if not data or len(data) < 5:
                logger.error('pvp failed. data len %d'%(len(data)))
                raise Exception()
            else:
                logger.info('pvp succeed. data len %d'%(len(data)))
            break
        except:
            logger.info('pvp failed, will sleep %d seconds'%(t*2))
            time.sleep(t*2)
            t += 1


if __name__ == '__main__':
    pvp()
