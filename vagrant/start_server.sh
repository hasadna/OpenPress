#!/usr/bin/env bash

cd /vagrant/backend
source /home/vagrant/venv/bin/activate
#killall python 2>/dev/null
#python manage.py syncdb --noinput


# ignore all errors since the user can pre-exist
#echo 'INSERT INTO "auth_user" VALUES(1,"pbkdf2_sha256$10000$fQ14C0o4Rccf$YE32evpiUOxASrEMiGQEtw4xglE1B0R3nm339rxY8Iw=","2014-02-17 22:16:51.758659",1,"root","","","admin@example.com",1,1,"2014-02-17 22:16:51.758659");' | python manage.py dbshell > /dev/null 2>&1 | :
#python  /vagrant/server/openpress.py runserver 0.0.0.0:8000