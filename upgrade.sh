cd /home/tianqi/psg
python upgradeEquip.py -i 1303542 -t 4 #ingma
python huodongThread.py -g
sh ./start_tax.sh
python upgradeEquip.py -d 20 -i 1303542 -t 4 #hqingma
sh ./start_tax.sh
#sh ./kill.sh magicThread.py
