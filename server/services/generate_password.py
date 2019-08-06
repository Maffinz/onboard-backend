import random
import string
import ibm_db
# import hashlib, uuid
from flask_bcrypt import generate_password_hash


def random_password(stringLength=10):
    """Generate a random string of fixed length and hashing it"""
    letters = string.ascii_lowercase
    password =  ''.join(random.choice(letters) for i in range(stringLength))
    return generate_password_hash(password, 10).decode('utf-8')

    # salt = uuid.uuid4().hex
    # return  hashlib.sha512(password.encode('utf-8') + salt.encode('utf-8')).hexdigest()
    # return hashed

def content(user=-1, err="None", status="bad"):
    return {
        "data": {
            "id": user,
        },
        "status": status,
        "error": err
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
