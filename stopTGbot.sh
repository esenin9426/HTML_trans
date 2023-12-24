#!/bin/bash

# Остановка контейнеров Docker Compose
docker-compose down

# Остановка python-процесса по сохраненному PID
if [ -f mypid.txt ]; then
    pid=$(cat mypid.txt)
    kill $pid
    rm mypid.txt
fi
