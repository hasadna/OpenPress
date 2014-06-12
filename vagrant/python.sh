#!/usr/bin/env bash

mkdir -p /var/lock/provision
export DEBIAN_FRONTEND=noninteractive

if [ ! -f /var/lock/provision/python_addons ]; then
    apt-get install -y -q python-pip python-dev python-numpy

    if [ $? == 0 ]; then
        touch /var/lock/provision/python_addons
    fi
fi


if [ ! -f /var/lock/provision/virtualenv ]; then
    pip install virtualenv
    rm -rf /home/vagrant/venv
    virtualenv /home/vagrant/venv
    source /home/vagrant/venv/bin/activate
    cd /vagrant
    pip install -r requirements.txt

    if [ $? == 0 ]; then
        touch /var/lock/provision/virtualenv
    fi
fi


if [ ! -f /var/lock/provision/django ]; then
    pip install django

    if [ $? == 0 ]; then
        touch /var/lock/provision/django
    fi
fi


