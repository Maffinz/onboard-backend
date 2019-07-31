from server import app
from flask import render_template, Flask, jsonify
import ibm_db
import json
from flask_cors import CORS
CORS(app)

# app.config['DB2_DATABASE'] = 'BLUDB'
# app.config['DB2_HOSTNAME'] = 'dashdb-txn-sbox-yp-dal09-04.services.dal.bluemix.net'
# app.config['DB2_PORT'] = 50000
# app.config['DB2_PROTOCOL'] = 'TCPIP'
# app.config['DB2_USER'] = 'gqf91534'
# app.config['DB2_PASSWORD'] = 'n8rbtmpr-0nfphqs'

# db = DB2(app) #You forgot that

# cur = db.connection.cursor()

conn = ibm_db.connect(
    'DATABASE=BLUDB;'
    'HOSTNAME=dashdb-txn-sbox-yp-dal09-04.services.dal.bluemix.net;'  # 127.0.0.1 or localhost works if it's local
    'PORT=50000;'
    'PROTOCOL=TCPIP;'
    'UID=gqf91534;'
    'PWD=n8rbtmpr-0nfphqs;',
    '',
    '')


""" """ 
@app.route("/api/get_users")
def get_users():
    stmt = ibm_db.exec_immediate(conn, "SELECT * from USER")
    data = []
    result = ibm_db.fetch_assoc(stmt)
    while result != False:
        data.append(result)
        result = ibm_db.fetch_assoc(stmt)
    # _dict = ibm_db.fetch_assoc(stmt)
    content = {'data': data}
    if conn:
        return jsonify(content)
    return "not connected"
    # return cur.execute("SELECT * FROM user")


@app.route("/api/get_events")
def get_events():
    stmt = ibm_db.exec_immediate(conn, "SELECT * from EVENT")
    data = []
    result = ibm_db.fetch_assoc(stmt)
    while result != False:
        data.append(result)
        result = ibm_db.fetch_assoc(stmt)
    # _dict = ibm_db.fetch_assoc(stmt)
    content = {'data': data}
    if conn:
        return jsonify(content)
    return "not connected"


# @app.route("/api/get_events")
# def get_events():
#     stmt = ibm_db.exec_immediate(conn, "SELECT * from EVENT")
#     data = []
#     result = ibm_db.fetch_assoc(stmt)
#     while result != False:
#         data.append(result)
#         result = ibm_db.fetch_assoc(stmt)
#     # _dict = ibm_db.fetch_assoc(stmt)
#     content = {'data': data}
#     if conn:
#         return jsonify(content)
#     return "not connected"


@app.route("/api/get_bios")
def get_bios():
    stmt = ibm_db.exec_immediate(conn, "SELECT * from INTERNBIO")
    data = []
    result = ibm_db.fetch_assoc(stmt)
    while result != False:
        data.append(result)
        result = ibm_db.fetch_assoc(stmt)
    # _dict = ibm_db.fetch_assoc(stmt)
    content = {'data': data}
    if conn:
        return jsonify(content)
    return "not connected"


@app.route("/api/get_resources")
def get_resources():
    stmt = ibm_db.exec_immediate(conn, "SELECT * from RESOURCES")
    data = []
    result = ibm_db.fetch_assoc(stmt)
    while result != False:
        data.append(result)
        result = ibm_db.fetch_assoc(stmt)
    # _dict = ibm_db.fetch_assoc(stmt)
    content = {'data': data}
    if conn:
        return jsonify(content)
    return "not connected"

@app.route("/api/get_employeetype")
def get_employeetype():
    stmt = ibm_db.exec_immediate(conn, "SELECT * from EMPLOYEETYPE")
    data = []
    result = ibm_db.fetch_assoc(stmt)
    while result != False:
        data.append(result)
        result = ibm_db.fetch_assoc(stmt)
    # _dict = ibm_db.fetch_assoc(stmt)
    content = {'data': data}
    if conn:
        return jsonify(content)
    return "not connected"

@app.route("/api/get_housing")
def get_housing():
    stmt = ibm_db.exec_immediate(conn, "SELECT * from HOUSING")
    data = []
    result = ibm_db.fetch_assoc(stmt)
    while result != False:
        data.append(result)
        result = ibm_db.fetch_assoc(stmt)
    # _dict = ibm_db.fetch_assoc(stmt)
    content = {'data': data}
    if conn:
        return jsonify(content)
    return "not connected"

@app.route("/api/get_sitelocation")
def get_sitelocation():
    stmt = ibm_db.exec_immediate(conn, "SELECT * from SITELOCATION")
    data = []
    result = ibm_db.fetch_assoc(stmt)
    while result != False:
        data.append(result)
        result = ibm_db.fetch_assoc(stmt)
    # _dict = ibm_db.fetch_assoc(stmt)
    content = {'data': data}
    if conn:
        return jsonify(content)
    return "not connected"

