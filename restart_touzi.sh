pgrep -U `id -u` -f "python touziThread.py" | xargs kill -9
python touziThread.py &
