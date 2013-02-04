pgrep -U `id -u` -f "python taxThread.py" | xargs kill -9
python taxThread.py &
