pgrep -U `id -u` -f "python jianzhuThread.py" | xargs kill -9
python jianzhuThread.py &
