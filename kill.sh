pgrep -U `id -u` -f "/usr/local/bin/python.*"$1 |xargs kill -9
