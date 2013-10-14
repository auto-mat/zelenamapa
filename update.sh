#!/bin/sh

git pull
env/bin/pip install -r requirements.txt
if [ "$1" = "migrate" ]; then
   echo "Backuping db..."
   mkdir db_backup
   env/bin/python manage.py dumpdata > db_backup/`date +"%y%m%d-%H:%M:%S"`-zmapa.json
   echo "Migrating..."
   env/bin/python manage.py migrate
fi
env/bin/python manage.py collectstatic --noinput
touch wsgi.py
