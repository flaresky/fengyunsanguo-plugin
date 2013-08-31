cd /home/zilong/psg
eid=1365073
did=963214   #hongjia
python upgradeEquip.py -i $eid -t 4
#python oneTimePerDay.py
sh ./start_tax.sh
#python downgradeEquip.py -i $did -t 100
#python upgradeEquip.py -d 20 -i 1105394 -t 4 #zifu2
#python upgradeEquip.py -d 20 -i 1777505 -t 4 #qingjia
#python upgradeEquip.py -d 20 -i 809359 #huangfu
#python upgradeEquip.py -d 20 -i 698158 -t 4 #zifu
#python upgradeEquip.py -d 20 -i 1230096 -t 4 #cuizi
python upgradeEquip.py -d 20 -i $eid -t 4
sh ./start_tax.sh
#python downgradeEquip.py -i $did -t 100
#sh ./kill.sh magicThread.py
