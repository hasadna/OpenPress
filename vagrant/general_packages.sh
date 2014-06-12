#!/usr/bin/env bash

mkdir -p /var/lock/provision
export DEBIAN_FRONTEND=noninteractive


if [ ! -f /var/lock/provision/apt_general_packages ]; then
    apt-get install -y -q build-essential cmake pkg-config libgtk2.0-dev curl

    if [ $? == 0 ]; then
        touch /var/lock/provision/apt_general_packages
    fi
fi

