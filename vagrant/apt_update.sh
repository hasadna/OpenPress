#!/usr/bin/env bash


mkdir -p /var/lock/provision
export DEBIAN_FRONTEND=noninteractive

if [ ! -f /var/lock/provision/apt_update ]; then
    apt-get update
    touch /var/lock/provision/apt_update
fi


if [ ! -f /var/lock/provision/apt_upgrade ]; then
    apt-get upgrade -y -q

    if [ $? == 0 ]; then
        touch /var/lock/provision/apt_upgrade
    fi
fi


