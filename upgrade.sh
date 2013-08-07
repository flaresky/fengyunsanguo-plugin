cd /home/zilong/psg
#python huodongThread.py -g
#python upgradeEquip.py -i 1105394 -t 4 #zifu2
#python upgradeEquip.py -i 1777505 -t 4 #qingjia
#python upgradeEquip.py -i 749122 -t 4 #qingma
#python upgradeEquip.py -i 1401340 #jian
#python upgradeEquip.py -i 809359 #huangfu
#python upgradeEquip.py -i 698158 -t 4 #zifu
#python upgradeEquip.py -i 1230096 -t 4 #cuizi
python upgradeEquip.py -i 2110398 -t 4 #hongpi
#python oneTimePerDay.py
sh ./start_tax.sh
#python downgradeEquip.py -i 839243 -t 100
#python upgradeEquip.py -d 20 -i 1105394 -t 4 #zifu2
#python upgradeEquip.py -d 20 -i 1777505 -t 4 #qingjia
#python upgradeEquip.py -d 20 -i 809359 #huangfu
#python upgradeEquip.py -d 20 -i 698158 -t 4 #zifu
#python upgradeEquip.py -d 20 -i 1230096 -t 4 #cuizi
python upgradeEquip.py -d 20 -i 2110398 -t 4 #hongpi
sh ./start_tax.sh
#python downgradeEquip.py -i 839243 -t 100
#sh ./kill.sh magicThread.py
