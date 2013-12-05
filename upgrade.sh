cd /home/tianqi/psg
#python upgradeEquip.py -i 398152 -t 4 #zifu1
#python huodongThread.py -g
python upgradeEquip.py -i 1383220 -t 4 #hongpi3
#python oneTimePerDay.py
sh ./start_tax.sh
python upgradeEquip.py -d 20 -i 1383220 -t 4 #hongpi3
#python upgradeEquip.py -d 20 -i 398152 -t 4 #zifu1

eid=2220238 #pifeng

#did=1230096

tax=0
quit=1
up_magic=93

downgradeEquip()
{
    if [[ -n "$did" ]]; then
        python downgradeEquip.py -i $did -t 100
    fi
}

upgradeEquip()
{
    if [[ -n "$eid" ]]; then
        python upgradeEquip.py -d $1 -i $eid -t $2
    fi
}

tax()
{
    if [[ "$tax" -gt 0 ]]; then
        sh ./start_tax.sh
    fi
}


if [[ "$1" -ge "$up_magic" ]]; then
    downgradeEquip
    upgradeEquip 0 4
    downgradeEquip
    tax
    upgradeEquip 20 3
    downgradeEquip
    tax
    upgradeEquip 5 2
    downgradeEquip

    if [[ "$quit" -gt 0 ]]; then
        sh ./kill.sh magicThread.py
    fi
fi
