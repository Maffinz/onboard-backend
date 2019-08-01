from server import app
from flask import render_template, Flask, jsonify, request
import ibm_db
import json
from flask_cors import CORS
CORS(app)

@app.route('/action/delete=<user_id>', methods = ['DELETE'])
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
    cont = {"status": "bad request"}
    sql_delete = "DELETE FROM user WHERE id={0}".format(user_id)
    if request.method == 'DELETE':
        cont = {"status": "ok"}
        stmt = ibm_db.exec_immediate(conn, sql_delete)

    return jsonify(cont)

    conn.close()

@app.route('/action/delete_bio=<user_id>', methods = ['DELETE'])
def bio_del(user_id):
    conn = ibm_db.connect(
    'DATABASE=BLUDB;'
    'HOSTNAME=dashdb-txn-sbox-yp-dal09-04.services.dal.bluemix.net;'  # 127.0.0.1 or localhost works if it's local
    'PORT=50000;'
    'PROTOCOL=TCPIP;'
    'UID=gqf91534;'
    'PWD=n8rbtmpr-0nfphqs;',
    '',
    '')

    cont = {"status": "ok"}

    sql_delete = "DELETE FROM internbio WHERE user_id={}".format(user_id)
    cont = {"status": "ok"}
    stmt = ibm_db.exec_immediate(conn, sql_delete)

    return jsonify(cont)
    conn.close()


