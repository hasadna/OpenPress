#!/usr/bin/env bash

mkdir -p /var/lock/provision
export DEBIAN_FRONTEND=noninteractive

# optional for OCR
if [ ! -f /var/lock/provision/ocr ]; then
    apt-get install -y -q libopencv-dev python-opencv opencv-doc

    if [ $? == 0 ]; then
        touch /var/lock/provision/ocr
    fi
 fi
