#!/bin/bash

# Запуск docker-compose в фоновом режиме
docker-compose up -d

# Ожидание запуска контейнеров (если необходимо)
sleep 5

# Запуск python-скрипта в фоновом режиме с записью логов в файл и сохранением PID процесса
nohup python3.10 main.py > mylog.log 2>&1 &
echo $! > mypid.txt
