from server import app
from flask import render_template, Flask, jsonify
import ibm_db
import json
from flask_cors import CORS
CORS(app)

@app.route("/api/get_users")
def get_users():
    conn = ibm_db.connect(
        'DATABASE=BLUDB;'
        'HOSTNAME=dashdb-txn-sbox-yp-dal09-04.services.dal.bluemix.net;'  # 127.0.0.1 or localhost works if it's local
        'PORT=50000;'
        'PROTOCOL=TCPIP;'
        'UID=gqf91534;'
        'PWD=n8rbtmpr-0nfphqs;',
        '',
        '')
    if conn:
        # stmt = ibm_db.exec_immediate(conn, "SELECT USER.ID, USER.NAME, USER.EMAIL, USER.PHONENUMBER, EMPLOYEETYPE.TYPE, SITELOCATION.SITE  FROM ((USER INNER JOIN EMPLOYEETYPE ON USER.EMPLOYEETYPE_ID = EMPLOYEETYPE.ID) INNER JOIN SITELOCATION ON USER.SITELOCATION_ID = SITELOCATION.ID)")
        stmt = ibm_db.exec_immediate(conn, "SELECT * FROM USER")
        data = []
        result = ibm_db.fetch_assoc(stmt)
        while result != False:
            data.append(result)
            result = ibm_db.fetch_assoc(stmt)
        content = {'data': data}
        ibm_db.close(conn)
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

@app.route("/api/get_bio=<user_id>")
def get_bios(user_id):
    conn = ibm_db.connect(
        'DATABASE=BLUDB;'
        'HOSTNAME=dashdb-txn-sbox-yp-dal09-04.services.dal.bluemix.net;'  # 127.0.0.1 or localhost works if it's local
        'PORT=50000;'
        'PROTOCOL=TCPIP;'
        'UID=gqf91534;'
        'PWD=n8rbtmpr-0nfphqs;',
        '',
        '')

    stmt = ibm_db.exec_immediate(conn, "SELECT * from INTERNBIO WHERE USER_ID={}".format(user_id))
    data = dict()
    result = ibm_db.fetch_assoc(stmt)
    # return result
    # while result != False:
    #     data[result[""]]
    #     result = ibm_db.fetch_assoc(stmt)
    # _dict = ibm_db.fetch_assoc(stmt)
    ibm_db.close(conn)
    content = {"data": { 
            "user": result,
        },
    }
    
    if conn:
        return jsonify(content)
    return "not connected"

# @app.route("/api/get_resources")
# def get_resources():
#     stmt = ibm_db.exec_immediate(conn, "SELECT * from RESOURCES")
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

@app.route("/api/get_employeetype")
def get_employeetype():
    conn = ibm_db.connect(
        'DATABASE=BLUDB;'
        'HOSTNAME=dashdb-txn-sbox-yp-dal09-04.services.dal.bluemix.net;'  # 127.0.0.1 or localhost works if it's local
        'PORT=50000;'
        'PROTOCOL=TCPIP;'
        'UID=gqf91534;'
        'PWD=n8rbtmpr-0nfphqs;',
        '',
        '')


    stmt = ibm_db.exec_immediate(conn, "SELECT * from EMPLOYEETYPE")
    data = {}
    result = ibm_db.fetch_assoc(stmt)
    while result != False:
        data[result["ID"]] = {"DATA": result["TYPE"], "ID": result["ID"]}
        result = ibm_db.fetch_assoc(stmt)
    # _dict = ibm_db.fetch_assoc(stmt)
    content = {'data': data, "status": "ok"}
    ibm_db.close(conn)
    if conn:
        return jsonify(content)
    return "not connected"

# @app.route("/api/get_housing")
# def get_housing():
#     stmt = ibm_db.exec_immediate(conn, "SELECT * from HOUSING")
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

@app.route("/api/get_sitelocation")
def get_sitelocation():
    conn = ibm_db.connect(
        'DATABASE=BLUDB;'
        'HOSTNAME=dashdb-txn-sbox-yp-dal09-04.services.dal.bluemix.net;'  # 127.0.0.1 or localhost works if it's local
        'PORT=50000;'
        'PROTOCOL=TCPIP;'
        'UID=gqf91534;'
        'PWD=n8rbtmpr-0nfphqs;',
        '',
        '')


    stmt = ibm_db.exec_immediate(conn, "SELECT * from SITELOCATION")
    data = dict()
    result = ibm_db.fetch_assoc(stmt)

    while result != False:
        data[result["ID"]] = {"DATA": result["SITE"], "ID": result["ID"]}
        result = ibm_db.fetch_assoc(stmt)
    # _dict = ibm_db.fetch_assoc(stmt)
    ibm_db.close(conn)
    content = {'data': data, "status": "ok"}
    if conn:
        return jsonify(content)
    return "not connected"
    