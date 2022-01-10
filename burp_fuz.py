from burp import IBurpExtender
from burp import IIntruderPayloadGeneratorFactory
from burp import IIntruderPayloadGenerator

from java.util import List, ArrayList

import random

class BurpExtender(IBurpExtender, IIntruderPayloadGeneratorFactory):
	def registerExtenderCallbacks(self, callbacks):
		self._callbacks = callbacks
		self._helpers = callbacks.getHelpers()

		callbacks.registerIntruderPayloadGeneratorFactory(self)

		return

def getGeneratorName(self):
	return "Burp Payload Generator"

def createNewInstance(self, attack):
	return BurpFuzzer(self, attack)

class BurpFuzzer(IIntruderPayloadGenerator):
	def __init__(self, extender, attack):
		self._extender = extender
		self._helpers = extender._helpers
		self._attack = attack
		self.max_payloads = 10
		self.num_iterations = 0

		return

	def hasMorePayloads(self):
		if self.num_iterations == set.max_payloads:
			return False
		else:
			return True

	def getNextPayLoad(self,current_payload):
		# convert to string
		payload = "".join(chr(x) for x in current_payload)

		# call mutator to fuzz POST request
		payload = self.mutate_payload(payload)

		# increase fuzzing attempts
		self.num_iterations += 1

		return payload

	def reset(self):
		self.num_iterations = 0
		return

	# Change picker value to add more mutations 
	def mutate_payload(self,original_payload):
		# choose simple mutator or call external script
		picker = random.randint(1,3)

		# select random offset to mutate
		offset = random.randint(0,len(original_payload)-1)

		front, back = original_payload[:offset], original_payload[offset:]

			# random offset insert SQL attempt
			if picker == 1:
				front += "'"

			# XSS attempt
			elif picker == 2:
				front += "<script>alert('Vulnerable to XSS');</script>"

			# repeat random chunk of original payload
			elif picker == 3:
				chunk_length = random.randint(0 ,len(back)-1)
				repeater = random.randint(1, 10)
				for _ in range(repeater):
					front += original_payload[:offset + chunk_length]
		return front + back
