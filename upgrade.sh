cd /home/tianqi/psg
eid=2164142 #qingpi
python upgradeEquip.py -i $eid -t 4
#python oneTimePerDay.py
sh ./start_tax.sh
#python downgradeEquip.py -i 1383220 -t 100
python upgradeEquip.py -d 20 -i $eid -t 4
sh ./start_tax.sh
#python downgradeEquip.py -i 1383220 -t 100
#sh ./kill.sh magicThread.py
