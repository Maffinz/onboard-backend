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

def content(user=None, user_data=None, err="None", status="bad"):
    code = 0
    if status == "bad":
        code = 300
        
    return {
        "data": user_data,
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

def getEditJSON():
    data = request.get_json()
    try:
        return {
            "USER": {
                # "NAME": data["data"]["user"]["NAME"],
                # "EMAIL": data["data"]["user"]["EMAIL"],
                # "EMPLOYEETYPE_ID": data["data"]["user"]["EMPLOYEETYPE_ID"],
                # "SITELOCATION_ID": data["data"]["user"]["SITELOCATION_ID"],
                "PHONENUMBER": data["data"]["user"]["PHONENUMBER"],
                "USER_ID": data["data"]["user"]["USER_ID"],
            },
            "INTERNBIO": {
                "HOUSING_ID": data["data"]["user"]["HOUSING_ID"],
                "DESCRIPTION": data["data"]["user"]["DESCRIPTION"],
                "SOCIAL_MEDIA": data["data"]["user"]["SOCIAL_MEDIA"],
                "CAR": data["data"]["user"]["CAR"],
                "SCHOOL": data["data"]["user"]["SCHOOL"],
                "SEX": data["data"]["user"]["SEX"],
                "EDUCATION_LEVEL": data["data"]["user"]["EDUCATION_LEVEL"]
            },
            
        }
    except:
        return {
            "USER": {
                "NAME": data["data"]["user"]["NAME"],
                "EMAIL": data["data"]["user"]["EMAIL"],
                "EMPLOYEETYPE_ID": data["data"]["user"]["EMPLOYEETYPE_ID"],
                "SITELOCATION_ID": data["data"]["user"]["SITELOCATION_ID"],
                "PHONENUMBER": data["data"]["user"]["PHONENUMBER"],
            },
            "INTERNBIO": {
                "HOUSING_ID": data["data"]["user"]["HOUSING_ID"],
                "DESCRIPTION": data["data"]["user"]["DESCRIPTION"],
                "SOCIAL_MEDIA": data["data"]["user"]["SOCIAL_MEDIA"],
                "CAR": data["data"]["user"]["CAR"],
                "SCHOOL": data["data"]["user"]["SCHOOL"],
                "SEX": data["data"]["user"]["SEX"],
                "EDUCATION_LEVEL": data["data"]["user"]["EDUCATION_LEVEL"]
            },
            "USER_ID": data["data"]["user"]["USER_ID"],
        }

def getEventJSON(): #Work on Adding Event to database
    #Get JSON
    data = request.get_json()
    try:
        return {
            "data": {

            }
        }
    except:
        return {
            "data": {

            }
        }

def reg_content(status=None, error=None, code=None):
    return {
        "data": {
            "user": None
        },
        "status": status,
        "error_info": {
            "error": error,
            "code": code
        }
    }

def check_email(email):
    conn = connect()

    sql = "SELECT * FROM USER WHERE user.email = {}".format(email)
    stmt = ibm_db.exec_immediate(conn, sql)


    ibm_db.close(conn)