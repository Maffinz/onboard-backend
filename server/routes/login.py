from server import app
from flask import render_template, Flask, jsonify, redirect, url_for, request, sessions
from http.cookies import SimpleCookie
import bcrypt
import ibm_db
import json
import secrets
from flask_cors import CORS
import datetime
CORS(app)

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

            if pword == upassword:
            #if bcrypt.checkpw(pword, upassword):
                addSession(uid)
                return c.output()
            else:
                return "Incorrect credentials"
        return session_login(uid)
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
    sessid = generateSessId()
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
            return setCookie(sess["SESSION"]) #renew cookie for 1 more hour
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
    c["session"]["expires"] = expiration.strftime("%a, %d-%b-%Y %H:%M:%S GMT")
    return c.output()

def generateSessId():
    return secrets.token_urlsafe(20)


@app.route('/logout')
def logout(uid=23):
    c["session"] = ""
    c["session"]["expires"] =(datetime.datetime.now() - datetime.timedelta(seconds=60*60)).strftime("%a, %d-%b-%Y %H:%M:%S GMT")
    
    ibm_db.exec_immediate(conn, f"DELETE from session WHERE USER_ID = {uid}")
    
    return "logged out"