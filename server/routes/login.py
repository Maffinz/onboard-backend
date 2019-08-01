from server import app
from flask import render_template, Flask, jsonify, redirect, url_for, request, session
from werkzeug.security import generate_password_hash, check_password_hash
import ibm_db
import json
from flask_cors import CORS
CORS(app)


# @app.route("/")
# def home:
#     if not session.get('logged_in'):
#         return "not logged in"
#     else:


@app.route("/login", methods = ['GET', 'POST'])
def checkPassword():
    conn = ibm_db.connect(
    'DATABASE=BLUDB;'
    'HOSTNAME=dashdb-txn-sbox-yp-dal09-04.services.dal.bluemix.net;'  # 127.0.0.1 or localhost works if it's local
    'PORT=50000;'
    'PROTOCOL=TCPIP;'
    'UID=gqf91534;'
    'PWD=n8rbtmpr-0nfphqs;',
    '',
    '')
    if request.method == 'POST':
        uname = request.form['username']
        pword = request.form['password']

        pword_stmt = ibm_db.exec_immediate(conn, f"SELECT password FROM user WHERE username == {uname}")
        password = ibm_db.fetch_assoc(pword_stmt)

        if check_password_hash(password, pword):
            user_stmt = ibm_db.exec_immediate(conn, f"SELECT id FROM user WHERE username == {uname}")
            userid = ibm_db.fetch_assoc(user_stmt)
            addSession(userid)
            return "Login successful"
        else:
            return "Incorrect credentials"
    conn.close()

def addSession(id):
    conn = ibm_db.connect(
    'DATABASE=BLUDB;'
    'HOSTNAME=dashdb-txn-sbox-yp-dal09-04.services.dal.bluemix.net;'  # 127.0.0.1 or localhost works if it's local
    'PORT=50000;'
    'PROTOCOL=TCPIP;'
    'UID=gqf91534;'
    'PWD=n8rbtmpr-0nfphqs;',
    '',
    '')
    result = ibm_db.exec_immediate(conn, f"INSERT INTO sessions (cookie, user_id) VALUES ("", {id})")
    if result:
        conn.close()
        return "Session added"