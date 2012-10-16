pgrep -U `id -u` -f "python.*"$1 |xargs kill -9
