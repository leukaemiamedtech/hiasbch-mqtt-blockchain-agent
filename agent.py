#!/usr/bin/env python3
""" HIASBCH Blockchain Agent Class

This object represents a HIAS iotJumpWay IoT Agent. HIAS IoT Agents process all
data coming from entities connected to the HIAS iotJumpWay broker using the
MQTT & Websocket machine to machine protocols.

MIT License

Copyright (c) 2021 Asociación de Investigacion en Inteligencia Artificial
Para la Leucemia Peter Moss

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files(the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and / or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

Contributors:
- Adam Milton-Barker

"""

from gevent import monkey
monkey.patch_all()

import json
import os
import psutil
import signal
import sys
import time

from flask import Flask, request, Response
from threading import Thread

from modules.AbstractAgent import AbstractAgent


class agent(AbstractAgent):
    """ HIASBCH Blockchain Agent Class

    HIASBCH Blockchain Agent Class process all data coming from IoT Agents
    and store immutable hashes in the HIASBCH Blockchain providing
    the functionality to perform data integrity checks.
    """

    def integrity_callback(self, topic, payload):
        """Called in the event of an integrity payload

        Args:
            topic (str): The topic the payload was sent to.
            payload (:obj:`str`): The payload.
        """

        data = json.loads(payload.decode("utf-8"))
        split_topic = topic.split("/")

        if split_topic[1] not in self.ignore_types:
            entity_type = split_topic[1][:-1]
        else:
            entity_type = split_topic[1]

        if entity_type in ["Robotics", "Application", "Staff"]:
            entity = split_topic[2]
        else:
            entity = split_topic[3]

        self.helpers.logger.info(
            "Received " + entity_type + " Integrity: " + str(data))

        attrs = self.get_attributes(entity_type, entity)
        bch = attrs["blockchain"]

        if not self.hiasbch.iotjumpway_access_check(bch):
            return

        entity = attrs["id"]
        location = attrs["location"]
        zone = attrs["zone"] if "zone" in attrs else "NA"

        Thread(target=self.hiasbch.store_hash, args=(
            data["_id"], self.hiasbch.hash(data), int(time.time()),
            location, entity, bch, entity_type), daemon=True).start()

        self.helpers.logger.info(entity_type + " " + entity + " status update OK")

    def respond(self, response_code, response):
        """ Returns the request repsonse """

        return Response(response=json.dumps(response, indent=4), status=response_code,
                        mimetype="application/json")

    def signal_handler(self, signal, frame):
        self.helpers.logger.info("Disconnecting")
        self.mqtt.disconnect()
        sys.exit(1)

app = Flask(__name__)
agent = agent()

@app.route('/About', methods=['GET'])
def about():
    """
    Returns Agent details
    Responds to GET requests sent to the North Port About API endpoint.
    """

    return agent.respond(200, {
        "Identifier": agent.credentials["iotJumpWay"]["entity"],
        "Host": agent.credentials["server"]["ip"],
        "NorthPort": agent.credentials["server"]["port"],
        "CPU": psutil.cpu_percent(),
        "Memory": psutil.virtual_memory()[2],
        "Diskspace": psutil.disk_usage('/').percent,
        "Temperature": psutil.sensors_temperatures()['coretemp'][0].current
    })

def main():

    signal.signal(signal.SIGINT, agent.signal_handler)
    signal.signal(signal.SIGTERM, agent.signal_handler)

    agent.hiascdi_connection()
    agent.hiasbch_connection()
    agent.mqtt_connection({
        "host": agent.credentials["iotJumpWay"]["host"],
        "port": agent.credentials["iotJumpWay"]["port"],
        "location": agent.credentials["iotJumpWay"]["location"],
        "zone": agent.credentials["iotJumpWay"]["zone"],
        "entity": agent.credentials["iotJumpWay"]["entity"],
        "name": agent.credentials["iotJumpWay"]["name"],
        "un": agent.credentials["iotJumpWay"]["un"],
        "up": agent.credentials["iotJumpWay"]["up"]
    })

    agent.mqtt.integrity_callback = agent.integrity_callback

    agent.threading()

    app.run(host=agent.helpers.credentials["server"]["ip"],
            port=agent.helpers.credentials["server"]["port"])

if __name__ == "__main__":
    main()
