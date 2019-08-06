import string
import ibm_db
from flask import request

from twilio.rest import Client

account_sid = "ACe343777b1ab47d98dd2c71e53a6b8030"
auth_token = "3e08fdfc79ed6fe1781664cbc6a5f2a7"

def send_sms(password, phonenumber):
    client = Client(account_sid, auth_token)

    message = client.messages \
                    .create(
                        body="You been added to OnBoard @ IBM\n Here is your password\n\n {}".format(password),
                        from_='+19564036594',
                        to='+1{}'.format(phonenumber)
                    )

    print(message.sid)