#!/usr/bin/env python
""" HIASBCH Blockchain Agent Class

HIASBCH Blockchain Agent Class process all data coming from IoT Agents and store
immutable hashes in the HIASBCH Blockchain providing the functionality
to perform data integrity checks.

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
import requests
import signal
import sys
import time
import threading

import os.path
sys.path.append(
	os.path.abspath(os.path.join(__file__,  "..", "..", "..", "..")))

from abc import ABC, abstractmethod
from datetime import datetime
from flask import Flask, request, Response
from threading import Thread

from components.agents.AbstractAgent import AbstractAgent


class Agent(AbstractAgent):
	""" Class representing a HIASBCH Blockchain Agent.

	This object represents a HIASBCH Blockchain Agent which
	process all data coming from IoT Agents and store immutable
	hashes in the HIASBCH Blockchain providing the functionality
	to perform data integrity checks.
	"""

	def __init__(self, protocol):
		super().__init__(protocol)

	def statusCallback(self, topic, payload):
		pass

	def lifeCallback(self, topic, payload):
		pass

	def sensorsCallback(self, topic, payload):
		pass

	def integrityCallback(self, topic, payload):
		"""Called in the event of an integrity payload

		Args:
			topic (str): The topic the payload was sent to.
			payload (:obj:`str`): The payload.
		"""

		data = json.loads(payload.decode("utf-8"))
		splitTopic = topic.split("/")

		if splitTopic[1] not in self.ignoreTypes:
			entityType = splitTopic[1][:-1]
		else:
			entityType = splitTopic[1]

		if entityType in ["Robotics", "Application", "Staff"]:
			entity = splitTopic[2]
		else:
			entity = splitTopic[3]

		self.helpers.logger.info(
			"Received " + entityType + " Integrity: " + str(data))

		attrs = self.getRequiredAttributes(entityType, entity)
		bch = attrs["blockchain"]

		if not self.hiasbch.iotJumpWayAccessCheck(bch):
			return

		entity = attrs["id"]
		location = attrs["location"]
		zone = attrs["zone"] if "zone" in attrs else "NA"

		Thread(target=self.hiasbch.storeHash, args=(data["_id"], self.hiasbch.hash(data), int(time.time()),
				location, entity, bch, entityType), daemon=True).start()

		self.helpers.logger.info(entityType + " " + entity + " status update OK")

	def life(self):
		""" Sends entity statistics to HIAS """

		cpu = psutil.cpu_percent()
		mem = psutil.virtual_memory()[2]
		hdd = psutil.disk_usage('/fserver').percent
		tmp = psutil.sensors_temperatures()['coretemp'][0].current
		r = requests.get('http://ipinfo.io/json?token=' +
					self.helpers.credentials["iotJumpWay"]["ipinfo"])
		data = r.json()
		location = data["loc"].split(',')

		self.mqtt.publish("Life", {
			"CPU": str(cpu),
			"Memory": str(mem),
			"Diskspace": str(hdd),
			"Temperature": str(tmp),
			"Latitude": str(location[0]),
			"Longitude": str(location[1])
		})

		self.helpers.logger.info("Agent life statistics published.")
		threading.Timer(300.0, self.life).start()

	def respond(self, responseCode, response):
		""" Returns the request repsonse """

		return Response(response=json.dumps(response, indent=4), status=responseCode,
						mimetype="application/json")

	def signal_handler(self, signal, frame):
		self.helpers.logger.info("Disconnecting")
		self.mqtt.disconnect()
		sys.exit(1)

app = Flask(__name__)
Agent = Agent("hiasbch")

@app.route('/About', methods=['GET'])
def about():
	"""
	Returns Agent details

	Responds to GET requests sent to the North Port About API endpoint.
	"""

	return Agent.respond(200, {
		"Identifier": Agent.credentials["iotJumpWay"]["entity"],
		"Host": Agent.credentials["server"]["ip"],
		"NorthPort": Agent.credentials["server"]["port"],
		"CPU": psutil.cpu_percent(),
		"Memory": psutil.virtual_memory()[2],
		"Diskspace": psutil.disk_usage('/').percent,
		"Temperature": psutil.sensors_temperatures()['coretemp'][0].current
	})

def main():

	signal.signal(signal.SIGINT, Agent.signal_handler)
	signal.signal(signal.SIGTERM, Agent.signal_handler)

	Agent.mongodbConn()
	Agent.hiascdiConn()
	Agent.hiasbchConn()
	Agent.mqttConn({
		"host": Agent.credentials["iotJumpWay"]["host"],
		"port": Agent.credentials["iotJumpWay"]["port"],
		"location": Agent.credentials["iotJumpWay"]["location"],
		"zone": Agent.credentials["iotJumpWay"]["zone"],
		"entity": Agent.credentials["iotJumpWay"]["entity"],
		"name": Agent.credentials["iotJumpWay"]["name"],
		"un": Agent.credentials["iotJumpWay"]["un"],
		"up": Agent.credentials["iotJumpWay"]["up"]
	})

	Agent.mqtt.integrityCallback = Agent.integrityCallback

	Thread(target=Agent.life, args=(), daemon=True).start()

	app.run(host=Agent.helpers.credentials["server"]["ip"],
			port=Agent.helpers.credentials["server"]["port"])

if __name__ == "__main__":
	main()
