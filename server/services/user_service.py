import string
import ibm_db
from flask import request

from twilio.rest import Client
from os import environ

account_sid = environ.get('TWILIO_SI')
auth_token = environ.get('TWILIO_AUTH')

def send_sms(password, phonenumber):
    client = Client(account_sid, auth_token)

    message = client.messages \
                    .create(
                        body="\nYou been added to OnBoard @ IBM\n Here is your password\n\n {}".format(password),
                        from_='+19564036594',
                        to='+1{0}'.format(phonenumber)
                    )

    print("Phone Number: " + phonenumber)
    print(message.sid)

def check_email(email):
    pass