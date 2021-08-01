#!/usr/bin/env python3
""" HIASBCH Helper Module

This module provides helper functions that allow the HIAS IoT Agents
to communicate with the HIASBCH Blockchain.

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

import bcrypt
import json
import sys
import time

from requests.auth import HTTPBasicAuth
from web3 import Web3


class hiasbch():
	""" HIASBCH Helper Module

	This module provides helper functions that allow the HIAS IoT
	Agents to communicate with the HIASBCH Blockchain.
	"""

	def __init__(self, helpers):
		""" Initializes the class. """

		self.helpers = helpers
		self.confs = self.helpers.confs
		self.credentials = self.helpers.credentials

		self.contractBalance = 5000

		self.helpers.logger.info("HIASBCH Class initialization complete.")

	def start(self):
		""" Connects to HIASBCH. """

		self.w3 = Web3(Web3.HTTPProvider("https://" + self.credentials["server"]["host"] + self.credentials["hiasbch"]["endpoint"], request_kwargs={
						'auth': HTTPBasicAuth(self.credentials["iotJumpWay"]["entity"],
												self.confs["agent"]["proxy"]["up"])}))
		self.authContract = self.w3.eth.contract(self.w3.toChecksumAddress(self.credentials["hiasbch"]["contracts"]["hias"]["contract"]),
												abi=json.dumps(self.credentials["hiasbch"]["contracts"]["hias"]["abi"]))
		self.iotContract = self.w3.eth.contract(self.w3.toChecksumAddress(self.credentials["hiasbch"]["contracts"]["iotJumpWay"]["contract"]),
												abi=json.dumps(self.credentials["hiasbch"]["contracts"]["iotJumpWay"]["abi"]))
		self.helpers.logger.info("HIASBCH connections started")

	def iotJumpWayAccessCheck(self, address):
		""" Checks sender is allowed access to the iotJumpWay Smart Contract """

		self.helpers.logger.info("HIASBCH checking " + address)
		if not self.iotContract.functions.accessAllowed(
					self.w3.toChecksumAddress(address)).call({
						'from': self.w3.toChecksumAddress(self.credentials["hiasbch"]["un"])}):
			return False
		else:
			return True

	def hash(self, data):
		""" Hashes Command data for data integrity. """

		hashString = ""

		for value in data:
			if value != "_id":
				hashString += str(data[value])

		hashed = bcrypt.hashpw(hashString.encode(), bcrypt.gensalt())

		return hashed

	def storeHash(self, id, hashed, at, inserter, identifier, to, typeof):
		""" Stores data hash in the iotJumpWay smart contract """

		try:
			txh = self.iotContract.functions.registerHash(id, hashed, at, 0, identifier, self.w3.toChecksumAddress(to)).transact({
														"from": self.w3.toChecksumAddress(self.credentials["hiasbch"]["un"]),
														"gas": 1000000})
			self.helpers.logger.info("HIASBCH Data Transaction OK!")
			txr = self.w3.eth.waitForTransactionReceipt(txh)
			if txr["status"] is 1:
				self.helpers.logger.info("HIASBCH Data Hash OK!")
			else:
				self.helpers.logger.error("HIASBCH Data Hash KO!")
		except:
			e = sys.exc_info()
			self.helpers.logger.error("HIASBCH Data Hash KO!")
			self.helpers.logger.error(str(e))
			self.helpers.logger.error(str(e))

	def getBalance(self, contract):
		""" Gets smart contract balance """

		try:
			balance = contract.functions.getBalance().call(
				{"from": self.w3.toChecksumAddress(self.confs["agent"]["hiasbch"]["un"])})
			balance = self.w3.fromWei(balance, "ether")
			self.helpers.logger.info("Get Balance OK!")
			return balance
		except:
			e = sys.exc_info()
			self.helpers.logger.error("Get Balance Failed!")
			self.helpers.logger.error(str(e))
			return False

	def replenish(self, contract, to, replenish):
		""" Replenishes the iotJumpWay smart contract """

		try:
			tx_hash = contract.functions.deposit(self.w3.toWei(replenish, "ether")).transact({
													"to": self.w3.toChecksumAddress(to),
													"from": self.w3.toChecksumAddress(self.confs["agent"]["hiasbch"]["un"]),
													"gas": 1000000,
													"value": self.w3.toWei(replenish, "ether")})
			self.helpers.logger.info("HIAS Blockchain Replenish Transaction OK! ")
			#self.helpers.logger.info(tx_hash)
			txr = self.w3.eth.waitForTransactionReceipt(tx_hash)
			if txr["status"] is 1:
				self.helpers.logger.info("HIAS Blockchain Data Hash OK!")
				#self.helpers.logger.info(str(txr))
			else:
				self.helpers.logger.error("HIAS Blockchain Data Hash KO!")
			return True
		except:
			e = sys.exc_info()
			self.helpers.logger.error("HIAS Blockchain Replenish Failed! ")
			self.helpers.logger.error(str(e))
			return False

