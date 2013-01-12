pgrep -U `id -u` -f "/usr/local/bin/python taxThread.py" | xargs kill -9
/usr/local/bin/python taxThread.py &
