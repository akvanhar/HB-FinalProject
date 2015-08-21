from twilio.rest import TwilioRestClient
import os

TWILIO_ACCOUNT_SID=os.environ['TWILIO_ACCOUNT_SID']
TWILIO_AUTH_TOKEN=os.environ['TWILIO_AUTH_TOKEN']
TWILIO_NUMBER=os.environ['TWILIO_NUMBER']
#authenticated TwilioRestClient

client = TwilioRestClient(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

to_number="+14152169086"

message = client.messages.create(from_=TWILIO_NUMBER, 
								 to=to_number, 
								 body="Robot Robot Robot.  Reeeh Rooooh.")

print message.sid