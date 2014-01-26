cd /home/droidhen/flaresky/psg

#eid=2300485 #qingfu
#eid=2495054 #hongfu
eid=2495053 #nvshu

did=1110926 #hongsu

enable=1
tax=0
tax_remain=0
quit=0
up_magic=94

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
        pgrep -U `id -u` -f "python taxThread.py" || python taxThread.py -x -r $tax_remain &
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
    main $1
fi
