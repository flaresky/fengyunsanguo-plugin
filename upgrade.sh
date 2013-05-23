cd /home/tianqi/psg
#python huodongThread.py -g
#python upgradeEquip.py -i 1105394 -t 4 #zifu2
#python upgradeEquip.py -i 1528439 -t 4 #qingjia
#python upgradeEquip.py -i 749122 -t 4 #qingma
#python upgradeEquip.py -i 1401340 #jian
#python upgradeEquip.py -i 809359 #huangfu
python upgradeEquip.py -i 1758407 -t 4 #zifu
#python upgradeEquip.py -i 1550918 -t 4 #qingpi
#python oneTimePerDay.py
sh ./start_tax.sh
#python upgradeEquip.py -d 20 -i 1105394 -t 4 #zifu2
#python upgradeEquip.py -d 20 -i 1528439 -t 4 #qingjia
#python upgradeEquip.py -d 20 -i 809359 #huangfu
python upgradeEquip.py -d 20 -i 1758407 -t 4 #zifu
sh ./start_tax.sh
#sh ./kill.sh magicThread.py
