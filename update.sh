#!/bin/bash
#version 0.3

app_name=zmapa
db_name=zelena_mapa_plzen1
source update_local.sh

set -e

if [ "$1" = "reinstall" ]; then
   rm env -rf
   virtualenv --no-site-packages env
fi

git pull
source env/bin/activate
env/bin/python env/bin/pip install --process-dependency-links -r requirements.txt
if [ "$1" = "migrate" ]; then
   echo "Backuping db..."
   mkdir -p db_backup
   sudo -u postgres pg_dump $db_name > db_backup/`date +"%y%m%d-%H:%M:%S"`.sql
   echo "Migrating..."
   env/bin/python ./manage.py migrate
fi
env/bin/python ./manage.py collectstatic --noinput
touch wsgi.py
