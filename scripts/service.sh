#!/bin/bash

FMSG="HIAS MQTT Blockchain IoT Agent service installation terminated!"

printf -- 'This script will install the HIAS MQTT Blockchain IoT Agent service on HIAS Core.\n';

read -p "Proceed (y/n)? " proceed
if [ "$proceed" = "Y" -o "$proceed" = "y" ]; then

        printf -- 'Installing HIAS MQTT Blockchain IoT Agent service.\n';
        sudo touch /lib/systemd/system/HIAS-MQTT-Blockchain-IoT-Agent.service
        echo "[Unit]" | sudo tee -a /lib/systemd/system/HIAS-MQTT-Blockchain-IoT-Agent.service
        echo "Description=HIAS-MQTT-Blockchain-IoT-Agent service" | sudo tee -a /lib/systemd/system/HIAS-MQTT-Blockchain-IoT-Agent.service
        echo "After=multi-user.target" | sudo tee -a /lib/systemd/system/HIAS-MQTT-Blockchain-IoT-Agent.service
        echo "After=HIASCDI.service" | sudo tee -a /lib/systemd/system/HIAS-MQTT-Blockchain-IoT-Agent.service
        echo "" | sudo tee -a /lib/systemd/system/HIAS-MQTT-Blockchain-IoT-Agent.service
        echo "[Service]" | sudo tee -a /lib/systemd/system/HIAS-MQTT-Blockchain-IoT-Agent.service
        echo "User=$USER" | sudo tee -a /lib/systemd/system/HIAS-MQTT-Blockchain-IoT-Agent.service
        echo "Type=simple" | sudo tee -a /lib/systemd/system/HIAS-MQTT-Blockchain-IoT-Agent.service
        echo "Restart=on-failure" | sudo tee -a /lib/systemd/system/HIAS-MQTT-Blockchain-IoT-Agent.service
        echo "ExecStart=/home/$USER/hias-core/components/agents/hiasbch/scripts/run.sh" | sudo tee -a /lib/systemd/system/HIAS-MQTT-Blockchain-IoT-Agent.service
        echo "" | sudo tee -a /lib/systemd/system/HIAS-MQTT-Blockchain-IoT-Agent.service
        echo "[Install]" | sudo tee -a /lib/systemd/system/HIAS-MQTT-Blockchain-IoT-Agent.service
        echo "WantedBy=multi-user.target" | sudo tee -a /lib/systemd/system/HIAS-MQTT-Blockchain-IoT-Agent.service
        echo "" | sudo tee -a /lib/systemd/system/HIAS-MQTT-Blockchain-IoT-Agent.service

        sudo systemctl enable HIAS-MQTT-Blockchain-IoT-Agent.service

        sudo sed -i -- "s/YourUser/$USER/g" /home/$USER/hias-core/components/agents/hiasbch/scripts/run.sh
        sudo chmod 744 /home/$USER/hias-core/components/agents/hiasbch/scripts/run.sh

        printf -- '\033[32m SUCCESS: HIAS MQTT Blockchain IoT Agent service installed! \033[0m\n';

else
    echo $FMSG;
    exit
fi