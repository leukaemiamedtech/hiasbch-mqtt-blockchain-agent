#!/bin/bash

FMSG="- HIAS MQTT Blockchain Agent installation terminated"

echo "This script will install the HIAS MQTT Blockchain Agent on your device."
read -p "Proceed (y/n)? " proceed

if [ "$proceed" = "Y" -o "$proceed" = "y" ]; then
    echo "- Installing HIAS MQTT Blockchain Agent"
    conda install -c anaconda bcrypt
    conda install flask
    conda install -c conda-forge paho-mqtt
    conda install psutil
    conda install requests
    conda install -c conda-forge web3
    printf -- '\033[32m SUCCESS: HIAS MQTT Blockchain Agent installed! \033[0m\n';
else
    echo $FMSG;
    exit
fi