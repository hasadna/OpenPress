#!/usr/bin/env bash

mkdir -p /var/lock/provision
export DEBIAN_FRONTEND=noninteractive

if [ ! -f /var/lock/provision/apache ]; then
    apt-get install -y -q apache2
    rm -rf /var/www
    ln -fs /vagrant /var/www

    if [ $? == 0 ]; then
        touch /var/lock/provision/apache
    fi
fi

