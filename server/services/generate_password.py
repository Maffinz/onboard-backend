import random
import string
import ibm_db
# import hashlib, uuid
from flask_bcrypt import generate_password_hash
from flask import request


def random_password(stringLength=10):
    """Generate a random string of fixed length and hashing it"""
    pass_info = list()
    letters = string.ascii_lowercase
    password =  ''.join(random.choice(letters) for i in range(stringLength))
    pass_info.append(password)
    pass_info.append(generate_password_hash(password, 10).decode('utf-8'))
    return pass_info

def content(user=-1, user_data=None, err="None", status="bad"):
    code = 0
    if status == "bad":
        code = 300
        
    return {
        "data": {
            "user": user_data,
        },
        "id": user,
        "status": status,
        "error": err,
        "code": code,
    }

def connect(database=None, hostname=None, port=None, protocol=None, uid=None, pwd=None):
    return ibm_db.connect(
        'DATABASE=BLUDB;'
        'HOSTNAME=dashdb-txn-sbox-yp-dal09-04.services.dal.bluemix.net;'  # 127.0.0.1 or localhost works if it's local
        'PORT=50000;'
        'PROTOCOL=TCPIP;'
        'UID=gqf91534;'
        'PWD=n8rbtmpr-0nfphqs;',
        '',
        '')

def getJSON():
    #Get JSON
    data = request.get_json()

    try:
        return {
            "name": data["data"]["user"]["NAME"],
            "email": data["data"]["user"]["EMAIL"],
            "phone_number": data["data"]["user"]["PHONENUMBER"],
            "employeeType_id": data["data"]["user"]["EMPLOYEETYPE_ID"],
            "siteLocation_id": data["data"]["user"]["SITELOCATION_ID"],
            "password": random_password() 
        }
    except:
        return {
            "data": {
                "user": "error"
            },
            "status": "bad",
            "error": "Wrong JSON format",
            "code": 200
        }
