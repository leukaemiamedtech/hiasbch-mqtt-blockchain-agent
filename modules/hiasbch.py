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

        self.auth_integrity_address = self.credentials["hiasbch"]["contracts"]["iotJumpWay"]["contract"]
        self.auth_integrity_abi = self.credentials["hiasbch"]["contracts"]["iotJumpWay"]["abi"]

        self.helpers.logger.info("HIASBCH Class initialization complete.")

    def start(self):
        """ Connects to HIASBCH. """

        self.w3 = Web3(Web3.HTTPProvider(
            "https://" + self.credentials["server"]["host"] \
                + self.credentials["hiasbch"]["endpoint"], request_kwargs={
                    'auth': HTTPBasicAuth(
                        self.credentials["iotJumpWay"]["entity"],
                        self.confs["agent"]["proxy"]["up"])}))

        self.integrity_contract = self.w3.eth.contract(
            self.w3.toChecksumAddress(self.auth_integrity_address),
            abi=json.dumps(self.auth_integrity_abi))

        self.helpers.logger.info("HIASBCH connections started")

    def iotjumpway_access_check(self, address):
        """ Checks sender is allowed access to the iotJumpWay Smart Contract """

        self.helpers.logger.info("HIASBCH checking " + address)
        if not self.integrity_contract.functions.accessAllowed(
                    self.w3.toChecksumAddress(address)).call({
                        'from': self.w3.toChecksumAddress(
                            self.credentials["hiasbch"]["un"])}):
            return False
        else:
            return True

    def hash(self, data):
        """ Hashes Command data for data integrity. """

        hashString = ""

        for value in data:
            if value != "_id":
                if type(data[value]) is dict:
                    for k, v in data[value].items():
                        hashString += k + str(v)
                else:
                    hashString += str(data[value])

        hashed = bcrypt.hashpw(hashString.encode(), bcrypt.gensalt())

        return hashed

    def store_hash(self, id, hashed, at, inserter, identifier, to, typeof):
        """ Stores data hash in the iotJumpWay smart contract """

        try:
            txh = self.integrity_contract.functions.registerHash(
                id, hashed, at, 0, identifier,
                self.w3.toChecksumAddress(to)).transact({
                    "from": self.w3.toChecksumAddress(
                        self.credentials["hiasbch"]["un"]),
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