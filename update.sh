#!/bin/bash

git pull
source env/bin/activate
pip install -r requirements.txt
if [ "$1" = "migrate" ]; then
   echo "Backuping db..."
   mkdir db_backup
   python ./manage.py dumpdata > db_backup/`date +"%y%m%d-%H:%M:%S"`-zmapa.json
   echo "Migrating..."
   python ./manage.py migrate
fi
python manage.py collectstatic --noinput
touch wsgi.py
