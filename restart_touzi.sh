pgrep -U `id -u` -f "/usr/local/bin/python touziThread.py" | xargs kill -9
/usr/local/bin/python touziThread.py &
