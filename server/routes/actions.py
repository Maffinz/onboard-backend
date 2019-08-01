from server import app
from flask import render_template, Flask, jsonify, request
import ibm_db
import json
from flask_cors import CORS
CORS(app)

@app.route('/test/test', methods = ['POST', 'GET', 'DELETE'])
def test():
    conn = ibm_db.connect(
    'DATABASE=BLUDB;'
    'HOSTNAME=dashdb-txn-sbox-yp-dal09-04.services.dal.bluemix.net;'  # 127.0.0.1 or localhost works if it's local
    'PORT=50000;'
    'PROTOCOL=TCPIP;'
    'UID=gqf91534;'
    'PWD=n8rbtmpr-0nfphqs;',
    '',
    '')
    ibm_db.close(conn)

    return "TEst Worked"

@app.route('/delete=<user_id>', methods = ['POST', 'GET', 'DELETE'])
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

    cont = {"status": "bad"}

    sql_delete_user = "DELETE FROM user WHERE id={0}".format(user_id)
    sql_delete_user_bio = "DELETE FROM internbio WHERE user_id={}".format(user_id)

    if conn:
        if request.method == 'DELETE':
            cont = {"status": "ok"}
            stmt = ibm_db.exec_immediate(conn, sql_delete_user)
            stmt = ibm_db.exec_immediate(conn, sql_delete_user_bio)
            ibm_db.close(conn)

        return jsonify(cont)

    # Not connected Should Render Template "No Access to Database"

@app.route('/add', methods = ['POST', 'GET'])
def add_user():
    data = request.get_json()

    conn = ibm_db.connect(
    'DATABASE=BLUDB;'
    'HOSTNAME=dashdb-txn-sbox-yp-dal09-04.services.dal.bluemix.net;'  # 127.0.0.1 or localhost works if it's local
    'PORT=50000;'
    'PROTOCOL=TCPIP;'
    'UID=gqf91534;'
    'PWD=n8rbtmpr-0nfphqs;',
    '',
    '')

    store_data = {
        "name" : data["data"]["user"]["name"],
        "email" : data["data"]["user"]["email"],
        "phone_number" : data["data"]["user"]["phone_number"],
        "employeeType_id" : data["data"]["user"]["employeeType_id"],
        "siteLocation_id" : data["data"]["user"]["siteLocation_id"]
    }

    sql_add_user = "INSERT INTO user (name, email, phonenumber, employeeType_id, siteLocation_id) VALUES ({}, {}, {}, {}, {})".format(
        store_data["name"], 
        store_data["email"], 
        store_data["phone_number"],
        store_data["employeeType_id"],
        store_data["siteLocation_id"])

    cont = {"status": "bad"}

    if conn:
        if request.method == 'POST':
            cont = {"status": "ok"}
            stmt = ibm_db.exec_immediate(conn, sql_add_user)

    ibm_db.close(conn)
    return jsonify(cont)
