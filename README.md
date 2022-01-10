# burpfuz - Simple burp extension for fuzzing

Made for the purpose of fuzzing pages w/ input to verify validation/errors/sanitization.

Fully customizable via bottom section of code:

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

Change randint values from (1,3) to higher value (i.e. 1,4 depending on what you want to add) for running more scripts.
Current code runs SQL, XSS, and random payloads.

Add to burpsuite via Extender tab.
1. Click add
2. Point to burp_fuz.py
3. Burp should load the extension

How to use:
1. Capture a request w/ a POST parameter
2. Send to Intruder
3. Specify positions
4. Go to Payloads tab
5. Payload type > Extension-generated > Select generator > BurpFuzzer
6. Start Attack
7. Look through your results :)
