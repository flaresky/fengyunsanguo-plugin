ps ux|grep -v grep|grep "python\|java" |grep $1|sed -e 's/\( \)\{1,\}/\1/g'|cut -d" " -f2| xargs kill -9
