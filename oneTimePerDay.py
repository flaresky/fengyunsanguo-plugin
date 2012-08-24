from sanguo import Sanguo
import time
import Logger

logger = Logger.getLogger()


retry = 10
t = 1
while t <= retry:
    try:
        sanguo = Sanguo()
        sanguo.login()
        data = sanguo.salary()
        sanguo.close()
        if len(data) < 50:
            logger.error('Salary failed. data len %d'%(len(data)))
            raise Exception()
        else:
            logger.info('Salary succeed. data len %d'%(len(data)))
        break
    except:
        logger.info('Salary failed, will sleep %d seconds'%(t*2))
        time.sleep(t*2)
        t += 1
