from server import app
from flask import render_template, Flask, jsonify, redirect, url_for, request, session
from http.cookies import SimpleCookie
from werkzeug.security import generate_password_hash, check_password_hash
import ibm_db
import json
from flask_cors import CORS
import datetime
CORS(app)

app.secret_key = "test"

#@app.route('/cookie')
def setCookie(session="test"):
    c = SimpleCookie()
    expiration = datetime.datetime.now() + datetime.timedelta(seconds=60*60)
    c['session'] = session
    c["session"]["path"] = "/"
    c["session"]["expires"] = expiration.strftime("%a, %d-%b-%Y %H:%M:%S EST")
    return c.output()

# @app.route("/")
# def home():
#     if not session.get("id") is None:
#         return "Logged in"
#     else:
#         return "Not logged in"


@app.route("/logintest", methods = ['GET', 'POST'])
def login(email = "simran.puri@ibm.com", pword = "tbgkytwfup"):
    conn = ibm_db.connect(
    'DATABASE=BLUDB;'
    'HOSTNAME=dashdb-txn-sbox-yp-dal09-04.services.dal.bluemix.net;'  # 127.0.0.1 or localhost works if it's local
    'PORT=50000;'
    'PROTOCOL=TCPIP;'
    'UID=gqf91534;'
    'PWD=n8rbtmpr-0nfphqs;',
    '',
    '')
    #if request.method == 'POST':
    get_user = ibm_db.exec_immediate(conn, f"SELECT id FROM user WHERE email = '{email}'")
    uid = ibm_db.fetch_assoc(get_user)
    # uid = user['id']

    get_password = ibm_db.exec_immediate(conn, f"SELECT password FROM password WHERE user_id = '{uid}'")
    upassword = ibm_db.fetch_assoc(get_password)
    # upassword = password['password']

    if upassword == password:
        addSession(uid)
        return "Login successful"
    else:
        return "Incorrect credentials"
    ibm_db.close(conn)

def addSession(uid):
    conn = ibm_db.connect(
    'DATABASE=BLUDB;'
    'HOSTNAME=dashdb-txn-sbox-yp-dal09-04.services.dal.bluemix.net;'  # 127.0.0.1 or localhost works if it's local
    'PORT=50000;'
    'PROTOCOL=TCPIP;'
    'UID=gqf91534;'
    'PWD=n8rbtmpr-0nfphqs;',
    '',
    '')
    sess = generateSession(uid)
    result = ibm_db.exec_immediate(conn, f"INSERT INTO sessions (session, user_id) VALUES ({sess}), {uid})")
    if result:
        conn.close()
        return "Session added"


def generateSession(uid):
    session[f"{uid}"] = "test"
    return session

def generate_token():
    return "test"

@app.route('/logout')
def logout(uid):
    sessid = session[f"{uid}"]
    c=SimpleCookie()
    c["session"] = ""
    c["session"]["expires"] =(datetime.datetime.now() - datetime.timedelta(seconds=60*60)).strftime("%a, %d-%b-%Y %H:%M:%S EST")
    session.pop(uid, None)
    
    return redirect(url_for('index'))