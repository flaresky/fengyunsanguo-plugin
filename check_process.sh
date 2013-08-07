#pgrep -u `id -u` -f tufei || python tufeiThread.py -e weiliao -t 1000 &
#pgrep -u `id -u` -f "trainingThread.py -a -e goujian" || python trainingThread.py -a -e goujian &
pgrep -u `id -u` -f xisi || python trainingThread.py -a -e xisi &
#pgrep -u `id -u` -f sunsangxiang || python trainingThread.py -a -e sunsangxiang -m 8 &
#pgrep -u `id -u` -f "trainingThread.py -e xiangyu" || python trainingThread.py -e xiangyu -l 130 &
pgrep -u `id -u` -f goujian || python trainingThread.py -a -e goujian -m 8 &
pgrep -u `id -u` -f guigu || python trainingThread.py -a -e guigu -m 8 &
pgrep -u `id -u` -f liubei || python trainingThread.py -a -e liubei -m 8 &
#pgrep -u `id -u` -f guanyu || python trainingThread.py -a -e guanyu -m 8 &
#pgrep -u `id -u` -f mozi || python trainingThread.py -a -e mozi -m 8 &
#pgrep -u `id -u` -f hanxin || python trainingThread.py -a -e hanxin -m 8 &
#pgrep -u `id -u` -f mulu || python trainingThread.py -a -e mulu -m 8 &
#pgrep -u `id -u` -f "trainingThread.py -e weiliao" || python trainingThread.py -e weiliao -m 8 -l 130 &

#pgrep -u `id -u` -f jianzhu || python jianzhuThread.py &
#pgrep -u `id -u` -f keji || python kejiThread.py &
pgrep -U `id -u` -f "python magicThread.py" || python magicThread.py -m 95 -u &
pgrep -u `id -u` -f weipaiThread || python weipaiThread.py &
