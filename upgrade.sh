cd /home/tianqi/psg
/usr/local/bin/python upgradeEquip.py -i 839243 -t 4 #hongjia4
#/usr/local/bin/python upgradeEquip.py -i 809359 -t 1 #huangfu
#/usr/local/bin/python upgradeEquip.py -i 615473 -t 4 #hongpi
sh ./start_tax.sh
/usr/local/bin/python upgradeEquip.py -d 20 -i 839243 -t 4 #hongjia4
#/usr/local/bin/python upgradeEquip.py -d 15 -i 809359 -t 1 #huangfu
#/usr/local/bin/python downgradeEquip.py -i 471179 -t 100
sh ./kill.sh magicThread.py
