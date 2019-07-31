from server import app
from flask import render_template, Flask, jsonify, request
import ibm_db
import json
from flask_cors import CORS
CORS(app)


conn = ibm_db.connect(
    'DATABASE=BLUDB;'
    'HOSTNAME=dashdb-txn-sbox-yp-dal09-04.services.dal.bluemix.net;'  # 127.0.0.1 or localhost works if it's local
    'PORT=50000;'
    'PROTOCOL=TCPIP;'
    'UID=gqf91534;'
    'PWD=n8rbtmpr-0nfphqs;',
    '',
    '')

@app.route('/user/<user_id>')
def user(user_id):
    pass

