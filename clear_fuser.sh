ps aux|grep -v grep|grep fuser|tr -s [:blank:]|cut -d" " -f2|xargs sudo kill -9
