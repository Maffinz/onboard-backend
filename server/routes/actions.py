from server import app
from flask import render_template, Flask, jsonify, request
import ibm_db
import json
from flask_cors import CORS
CORS(app)

@app.route('/action/delete=<user_id>', methods = ['GET', 'POST', 'DELETE'])
def user(user_id):
    conn = ibm_db.connect(
    'DATABASE=BLUDB;'
    'HOSTNAME=dashdb-txn-sbox-yp-dal09-04.services.dal.bluemix.net;'  # 127.0.0.1 or localhost works if it's local
    'PORT=50000;'
    'PROTOCOL=TCPIP;'
    'UID=gqf91534;'
    'PWD=n8rbtmpr-0nfphqs;',
    '',
    '')

    sql_delete = "DELETE FROM user WHERE id={0}".format(user_id)
    sql_get = "SELECT FROM user WHERE id={0}".format(user_id)

    # sql_POST = "INSERT INTO 'user' WHERE 'id'={0}".format(user_id)
    # if request.method == 'GET':
    #     #Do Get Request
    #     pass
    # if request.method == 'POST':
    #     #Do Post Request
    #     pass
    if request.method == 'DELETE':
        cont = {"STATUS": "Ok"}
        stmt = ibm_db.exec_immediate(conn, sql_delete)
        return jsonify(cont)

    conn.close()

