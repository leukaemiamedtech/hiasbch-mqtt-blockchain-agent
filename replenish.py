#!/usr/bin/env python
""" HIASBCH Replenish Service.

The HIASBCH Replenish Service is used to replenish HIAS Smart Contracts
with Ether so that they can fulfill their purpose.

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

import time
import os
import sys

from modules.helpers import helpers
from modules.hiasbch import hiasbch


class replenish():
	""" HIASBCH Replenish Service Class

	The replenish module is used to replenish HIAS Smart Contracts
	with Ether so that they can function.
	"""

	def __init__(self):
		""" Initializes the class. """

		self.helpers = helpers("Replenish")
		self.confs = self.helpers.confs
		self.credentials = self.helpers.credentials

		self.hiasbch = hiasbch(self.helpers)
		self.hiasbch.start()
		self.hiasbch.w3.geth.personal.unlockAccount(
			self.hiasbch.w3.toChecksumAddress(self.confs["agent"]["hiasbch"]["un"]),
			self.confs["agent"]["hiasbch"]["up"], 0)

		self.contractBalance = 5000

		self.helpers.logger.info("replenish Class initialization complete.")


replenish = replenish()

while True:
	abalance = replenish.hiasbch.getBalance(replenish.hiasbch.authContract)
	replenish.helpers.logger.info(
		"Auth Contract (" + replenish.credentials["hiasbch"]["contracts"]["hias"]["contract"] + ") has a balance of " + str(abalance) + " HIAS Ether")

	if abalance < replenish.hiasbch.contractBalance:
		replenishment = replenish.hiasbch.contractBalance - abalance
		if replenish.hiasbch.replenish(
						replenish.hiasbch.authContract, replenish.credentials["hiasbch"]["contracts"]["hias"]["contract"], replenishment):
					replenish.helpers.logger.info(
						"Auth Contract (" + replenish.credentials["hiasbch"]["contracts"]["hias"]["contract"] + ") balanced replenished to " + str(replenish.hiasbch.contractBalance) + " HIAS Ether")

	ibalance = replenish.hiasbch.getBalance(replenish.hiasbch.iotContract)
	replenish.helpers.logger.info(
		"iotJumpWay Contract (" + replenish.credentials["hiasbch"]["contracts"]["iotJumpWay"]["contract"] + ") has a balance of " + str(ibalance) + " HIAS Ether")

	if ibalance < replenish.hiasbch.contractBalance:
		replenishment = replenish.hiasbch.contractBalance - ibalance
		if replenish.hiasbch.replenish(
				replenish.hiasbch.iotContract, replenish.credentials["hiasbch"]["contracts"]["iotJumpWay"]["contract"] , replenishment):
					replenish.helpers.logger.info(
						"iotJumpWay Contract (" + replenish.credentials["hiasbch"]["contracts"]["iotJumpWay"]["contract"] + ") balanced replenished to " + str(replenish.hiasbch.contractBalance) + " HIAS Ether")

	time.sleep(300)
