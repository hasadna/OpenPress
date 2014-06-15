#!/usr/bin/env bash

mkdir -p /var/lock/provision
export DEBIAN_FRONTEND=noninteractive



if [ ! -f /var/lock/provision/git ]; then
    apt-get install -y -q git
    git clone https://github.com/hasadna/OpenPress.git ~/OpenPress

    if [ $? == 0 ]; then
        touch /var/lock/provision/git
    fi
fi