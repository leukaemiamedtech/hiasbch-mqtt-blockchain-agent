#!/usr/bin/env python3
""" HIAS iotJumpWay Agent Abstract Class

HIAS IoT Agents process all data coming from entities connected to the HIAS
iotJumpWay brokers.

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

import json
import psutil
import requests
import ssl
import threading

from abc import ABC, abstractmethod

from modules.helpers import helpers
from modules.hiasbch import hiasbch
from modules.hiascdi import hiascdi
from modules.mqtt import mqtt


class AbstractAgent(ABC):
	""" Abstract class representing a HIAS iotJumpWay IoT Agent.

	This object represents a HIAS iotJumpWay IoT Agent. HIAS IoT Agents
	process all data coming from entities connected to the HIAS iotJumpWay
	broker using the various machine to machine protocols.
	"""

	def __init__(self):
		"Initializes the AbstractAgent object."

		self.hiascdi = None
		self.hiashdi = None
		self.mqtt = None

		self.appTypes = ["Robotics", "Application", "Staff"]
		self.ignoreTypes = ["Robotics", "HIASCDI", "HIASHDI", "Staff"]

		self.helpers = helpers("Agent")
		self.confs = self.helpers.confs
		self.credentials = self.helpers.credentials

		self.helpers.logger.info("Agent initialization complete.")

	def hiascdiConn(self):
		"""Instantiates the HIASCDI Contextual Data Interface connection. """

		self.hiascdi = hiascdi(self.helpers)

		self.helpers.logger.info(
			"HIASCDI Contextual Data Interface connection instantiated.")

	def mqttConn(self, credentials):
		"""Initializes the HIAS MQTT connection. """

		self.mqtt = mqtt(self.helpers, "Agent", credentials)
		self.mqtt.configure()
		self.mqtt.start()

		self.helpers.logger.info(
			"HIAS iotJumpWay MQTT Broker connection created.")

	def hiasbchConn(self):
		"""Initializes the HIASBCH connection. """

		self.hiasbch = hiasbch(self.helpers)
		self.hiasbch.start()
		self.hiasbch.w3.geth.personal.unlockAccount(
			self.hiasbch.w3.toChecksumAddress(self.credentials["hiasbch"]["un"]),
			self.credentials["hiasbch"]["up"], 0)

		self.helpers.logger.info(
			"HIAS HIASBCH Blockchain connection created.")

	def getRequiredAttributes(self, entityType, entity):
		"""Gets entity attributes from HIASCDI.

		Args:
			entityType (str): The HIASCDI Entity type.
			entity (str): The entity id.

		Returns:
			dict: Required entity attributes

		"""

		attrs = self.hiascdi.getRequiredAttributes(entityType, entity)

		rattrs = {}

		if entityType in self.appTypes:
			rattrs["id"] = attrs["id"]
			rattrs["type"] = attrs["type"]
			rattrs["blockchain"] = attrs["authenticationBlockchainUser"]["value"]
			rattrs["location"] = attrs["networkLocation"]["value"]
		else:
			rattrs["id"] = attrs["id"]
			rattrs["type"] = attrs["type"]
			rattrs["blockchain"] = attrs["authenticationBlockchainUser"]["value"]
			rattrs["location"] = attrs["networkLocation"]["value"]
			rattrs["zone"] = attrs["networkZone"]["value"]

		return rattrs

	def life(self):
		""" Publishes entity statistics to HIAS. """

		cpu = psutil.cpu_percent()
		mem = psutil.virtual_memory()[2]
		hdd = psutil.disk_usage('/').percent
		tmp = psutil.sensors_temperatures()['coretemp'][0].current
		r = requests.get('http://ipinfo.io/json?token=' +
					self.credentials["iotJumpWay"]["ipinfo"])
		data = r.json()

		if "loc" in data:
			location = data["loc"].split(',')
		else:
			location = ["0.0", "0.0"]

		self.mqtt.publish("Life", {
			"CPU": float(cpu),
			"Memory": float(mem),
			"Diskspace": float(hdd),
			"Temperature": float(tmp),
			"Latitude": float(location[0]),
			"Longitude": float(location[1])
		})

		self.helpers.logger.info("Agent life statistics published.")
		threading.Timer(300.0, self.life).start()

	def threading(self):
		""" Creates required module threads. """

		# Life thread
		threading.Timer(10.0, self.life).start()
