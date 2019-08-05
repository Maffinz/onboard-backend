from server import app
from flask import render_template, Flask, jsonify, redirect, url_for, request, session
from http.cookies import SimpleCookie
import bcrypt
import ibm_db
import json
from flask_cors import CORS
import datetime
CORS(app)

app.secret_key = "test"
c = SimpleCookie()

# @app.route("/")
# def home():
#     if not session.get("id") is None:
#         return "Logged in"
#     else:
#         return "Not logged in"


conn = ibm_db.connect(
    'DATABASE=BLUDB;'
    'HOSTNAME=dashdb-txn-sbox-yp-dal09-04.services.dal.bluemix.net;'  # 127.0.0.1 or localhost works if it's local
    'PORT=50000;'
    'PROTOCOL=TCPIP;'
    'UID=gqf91534;'
    'PWD=n8rbtmpr-0nfphqs;',
    '',
    '')

@app.route("/logintest", methods = ['GET', 'POST'])
def login(email = "simran.puri@ibm.com", pword = "tbgkytwfup"):
    if email:
        get_user = ibm_db.exec_immediate(conn, f"SELECT * FROM user WHERE email = '{email}'")
        user = ibm_db.fetch_assoc(get_user)
        uid = user["ID"]

        if pword:
            get_password = ibm_db.exec_immediate(conn, f"SELECT password FROM password WHERE user_id = {uid}")
            password = ibm_db.fetch_assoc(get_password)
            upassword = password["PASSWORD"]

            if bcrypt.check_password_hash(pword, upassword):
                addSession(uid)
                return c.output()
            else:
                return "Incorrect credentials"
        session_login(uid)
        return c.output()
    else:
        return "Insufficient login data"
    # ibm_db.close(conn)


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
    sessid = "test"
    result = ibm_db.exec_immediate(conn, f"INSERT INTO session (session, user_id) VALUES ('{sessid}', {uid})")
    if result:
        setCookie(sessid)
        return sessid
    return None

def session_login(uid):
    sess = findsess(uid)
    if sess:
        currentuser = finduser(sess["USER_ID"])
        if currentuser:
            setCookie(sess["SESSION"]) #renew cookie for 1 more hour
            return currentuser, "Logged in"
        return "No user found"
    return "No session found"


def findsess(uid):
    get_sess = ibm_db.exec_immediate(conn, f"SELECT * FROM session WHERE user_id = {uid}")
    sess = ibm_db.fetch_assoc(get_sess)
    if sess:
        return sess
    return None

def finduser(uid):
    get_user = ibm_db.exec_immediate(conn, f"SELECT * FROM user WHERE id = {uid}")
    user = ibm_db.fetch_assoc(get_user)
    if user:
        return user
    return None
    
def setCookie(sessid):
    expiration = datetime.datetime.now() + datetime.timedelta(seconds=60*60)
    c["session"] = sessid
    c["session"]["expires"] = expiration.strftime("%a, %d-%b-%Y %H:%M:%S EST")
    return c.output()

# def generateSession(uid):
#     session[f"'{uid}''"] = "test"
#     return session


@app.route('/logout')
def logout(uid=23):
    # sessid = findsess(uid)["SESSION"]
    c["session"] = ""
    session["expires"] =(datetime.datetime.now() - datetime.timedelta(seconds=60*60)).strftime("%a, %d-%b-%Y %H:%M:%S EST")
    
    ibm_db.exec_immediate(conn, f"DELETE from session WHERE user_id = {uid}")
    
    return "logged out"