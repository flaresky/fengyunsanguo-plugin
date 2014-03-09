cd /home/droidhen/flaresky/psg

#eid=2534749 #renhuang
eid=2531189 #nvsu

#did=2072668 #qingpi
did=1781505 #baihu

enable=1
jinglian_level=150
tax=1
tax_remain=38
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

jinglian()
{
    if [[ "$jinglian_level" -gt 0 ]]; then
        pgrep -U `id -u` -f "python jinglianEquip.py" || python jinglianEquip.py -i $eid -l $jinglian_level &
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
        jinglian

        if [[ "$quit" -gt 0 ]]; then
            sh ./kill.sh magicThread.py
        fi
    fi
}

if [[ "$enable" -gt 0 ]]; then
    main $1
fi
