#!/usr/bin/env bash

apt-get update
apt-get upgrade
apt-get install -y ubuntu-desktop
apt-get install -y apache2
pip install django
rm -rf /var/www
ln -fs /vagrant /var/www