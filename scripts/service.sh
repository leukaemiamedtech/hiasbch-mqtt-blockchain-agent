#!/bin/bash

FMSG="- HIASBCH MQTT Blockchain Agent service installation terminated"

read -p "? This script will install the HIASBCH MQTT Blockchain Agent service on your device. Are you ready (y/n)? " cmsg

if [ "$cmsg" = "Y" -o "$cmsg" = "y" ]; then
	echo "- Installing HIASBCH MQTT Blockchain Agent service"
	sudo touch /lib/systemd/system/HIASBCH-MQTT-Blockchain-Agent.service
	echo "[Unit]" | sudo tee -a /lib/systemd/system/HIASBCH-MQTT-Blockchain-Agent.service
	echo "Description=HIASBCH MQTT Blockchain Agent service" | sudo tee -a /lib/systemd/system/HIASBCH-MQTT-Blockchain-Agent.service
	echo "After=multi-user.target" | sudo tee -a /lib/systemd/system/HIASBCH-MQTT-Blockchain-Agent.service
	echo "After=HIASCDI.service" | sudo tee -a /lib/systemd/system/HIASBCH-MQTT-Blockchain-Agent.service
	echo "" | sudo tee -a /lib/systemd/system/HIASBCH-MQTT-Blockchain-Agent.service
	echo "[Service]" | sudo tee -a /lib/systemd/system/HIASBCH-MQTT-Blockchain-Agent.service
	echo "User=$USER" | sudo tee -a /lib/systemd/system/HIASBCH-MQTT-Blockchain-Agent.service
	echo "Type=simple" | sudo tee -a /lib/systemd/system/HIASBCH-MQTT-Blockchain-Agent.service
	echo "Restart=on-failure" | sudo tee -a /lib/systemd/system/HIASBCH-MQTT-Blockchain-Agent.service
	echo "ExecStart=/usr/bin/python3 /home/$USER/HIAS/components/agents/mqtt/agent.py" | sudo tee -a /lib/systemd/system/HIASBCH-MQTT-Blockchain-Agent.service
	echo "" | sudo tee -a /lib/systemd/system/HIASBCH-MQTT-Blockchain-Agent.service
	echo "[Install]" | sudo tee -a /lib/systemd/system/HIASBCH-MQTT-Blockchain-Agent.service
	echo "WantedBy=multi-user.target" | sudo tee -a /lib/systemd/system/HIASBCH-MQTT-Blockchain-Agent.service
	echo "" | sudo tee -a /lib/systemd/system/HIASBCH-MQTT-Blockchain-Agent.service

	sudo systemctl enable HIASBCH-MQTT-Blockchain-Agent.service
	sudo systemctl start HIASBCH-MQTT-Blockchain-Agent.service

	echo "- Installed HIASBCH MQTT Blockchain Agent service!";
	exit 0
else
	echo $FMSG;
	exit 1
fi