cd /home/tianqi/psg

eid=2438797 #hongfu
#eid=2391732 #pi

#did=1758407 #zifu

enable=1
tax=1
quit=0
up_magic=95

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

main()
{
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
}

if [[ "$enable" -gt 0 ]]; then
    main
fi
