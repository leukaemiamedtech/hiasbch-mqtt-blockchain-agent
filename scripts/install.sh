#!/bin/bash

FMSG="- HIAS MQTT IoT Agent installation terminated"

echo "This script will install the HIAS MQTT IoT Agent on your device."
read -p "Proceed (y/n)? " proceed

if [ "$proceed" = "Y" -o "$proceed" = "y" ]; then
    echo "- Installing HIAS MQTT IoT Agent"
    pip3 install --user bcrypt
    pip3 install --user flask
    pip3 install --user paho-mqtt
    pip3 install --user psutil
    pip3 install --user requests
    pip3 install --user web3
    echo "- HIAS MQTT IoT Agent installed!"
else
    echo $FMSG;
    exit
fi