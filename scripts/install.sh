#!/bin/bash

FMSG="- HIASBCH MQTT Blockchain Agent installation terminated"

read -p "? This script will install the HIASBCH MQTT Blockchain Agent on your device. Are you ready (y/n)? " cmsg

if [ "$cmsg" = "Y" -o "$cmsg" = "y" ]; then
    echo "- Installing HIASBCH MQTT Blockchain Agent"
	pip3 install --user flask
	pip3 install --user gevent
	pip3 install --user psutil
	pip3 install --user requests
	pip3 install --user web3
	pip3 install --user gevent
    echo "- HIASBCH MQTT Blockchain Agent installed!"
else
    echo $FMSG;
    exit
fi