#!/bin/bash

FMSG="- HIASBCH MQTT Blockchain Agent service installation terminated"

echo "This script will install the HIASBCH MQTT Blockchain Agent service on your device."
read -p "Proceed (y/n)? " proceed

if [ "$proceed" = "Y" -o "$proceed" = "y" ]; then
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
	echo "ExecStart=/usr/bin/python3 /home/$USER/HIAS/components/agents/hiasbch/agent.py" | sudo tee -a /lib/systemd/system/HIASBCH-MQTT-Blockchain-Agent.service
	echo "" | sudo tee -a /lib/systemd/system/HIASBCH-MQTT-Blockchain-Agent.service
	echo "[Install]" | sudo tee -a /lib/systemd/system/HIASBCH-MQTT-Blockchain-Agent.service
	echo "WantedBy=multi-user.target" | sudo tee -a /lib/systemd/system/HIASBCH-MQTT-Blockchain-Agent.service
	echo "" | sudo tee -a /lib/systemd/system/HIASBCH-MQTT-Blockchain-Agent.service

	echo "- Installing HIASBCH MQTT Blockchain Agent Replenish service"
	sudo touch /lib/systemd/system/HIASBCH-MQTT-Blockchain-Agent-Replenish.service
	echo "[Unit]" | sudo tee -a /lib/systemd/system/HIASBCH-MQTT-Blockchain-Agent-Replenish.service
	echo "Description=HIASBCH MQTT Blockchain Agent service" | sudo tee -a /lib/systemd/system/HIASBCH-MQTT-Blockchain-Agent-Replenish.service
	echo "After=multi-user.target" | sudo tee -a /lib/systemd/system/HIASBCH-MQTT-Blockchain-Agent-Replenish.service
	echo "After=HIASCDI.service" | sudo tee -a /lib/systemd/system/HIASBCH-MQTT-Blockchain-Agent-Replenish.service
	echo "" | sudo tee -a /lib/systemd/system/HIASBCH-MQTT-Blockchain-Agent-Replenish.service
	echo "[Service]" | sudo tee -a /lib/systemd/system/HIASBCH-MQTT-Blockchain-Agent-Replenish.service
	echo "User=$USER" | sudo tee -a /lib/systemd/system/HIASBCH-MQTT-Blockchain-Agent-Replenish.service
	echo "Type=simple" | sudo tee -a /lib/systemd/system/HIASBCH-MQTT-Blockchain-Agent-Replenish.service
	echo "Restart=on-failure" | sudo tee -a /lib/systemd/system/HIASBCH-MQTT-Blockchain-Agent-Replenish.service
	echo "ExecStart=/usr/bin/python3 /home/$USER/HIAS/components/agents/hiasbch/replenish.py" | sudo tee -a /lib/systemd/system/HIASBCH-MQTT-Blockchain-Agent-Replenish.service
	echo "" | sudo tee -a /lib/systemd/system/HIASBCH-MQTT-Blockchain-Agent-Replenish.service
	echo "[Install]" | sudo tee -a /lib/systemd/system/HIASBCH-MQTT-Blockchain-Agent-Replenish.service
	echo "WantedBy=multi-user.target" | sudo tee -a /lib/systemd/system/HIASBCH-MQTT-Blockchain-Agent-Replenish.service
	echo "" | sudo tee -a /lib/systemd/system/HIASBCH-MQTT-Blockchain-Agent-Replenish.service

	sudo systemctl enable HIASBCH-MQTT-Blockchain-Agent.service
	sudo systemctl start HIASBCH-MQTT-Blockchain-Agent.service

	sudo systemctl enable HIASBCH-MQTT-Blockchain-Agent-Replenish.service
	sudo systemctl start HIASBCH-MQTT-Blockchain-Agent-Replenish.service

	echo "- Installed HIASBCH MQTT Blockchain Agent service!";
	exit 0
else
	echo $FMSG;
	exit 1
fi