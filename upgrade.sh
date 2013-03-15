cd /home/tianqi/psg
#python upgradeEquip.py -i 398152 -t 4 #zifu1
#python huodongThread.py -g
python upgradeEquip.py -i 1383220 -t 4 #hongpi3
#python oneTimePerDay.py
sh ./start_tax.sh
python upgradeEquip.py -d 20 -i 1383220 -t 4 #hongpi3
#python upgradeEquip.py -d 20 -i 398152 -t 4 #zifu1
sh ./start_tax.sh
sh ./kill.sh magicThread.py
