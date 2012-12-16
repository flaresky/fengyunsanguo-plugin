cd /home/tianqi/psg
python upgradeEquip.py -i 839243 -t 4 #hongjia4
#python upgradeEquip.py -i 809359 -t 1 #huangfu
#python upgradeEquip.py -i 615473 -t 4 #hongpi
sh ./start_tax.sh
python upgradeEquip.py -d 20 -i 839243 -t 4 #hongjia4
#python upgradeEquip.py -d 15 -i 809359 -t 1 #huangfu
#python downgradeEquip.py -i 471179 -t 100
#python downgradeEquip.py -i 225028 -t 100
sh ./kill.sh magicThread.py
