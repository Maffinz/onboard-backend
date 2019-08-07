from server import app
from flask import render_template, Flask, jsonify, redirect, url_for, request, sessions
from http.cookies import SimpleCookie
import bcrypt
import ibm_db
import json
import secrets
from flask_cors import CORS
import datetime
import os
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

@app.route("/login", methods = ['GET', 'POST'])
def login():
    data = request.get_json()
    if request.method == 'POST':
        credentials = data["data"]["credentials"]
        email = credentials.get("email")
        pword = credentials.get("password")  
        
        get_user = ibm_db.exec_immediate(conn, f"SELECT * FROM user WHERE email = '{email}'")
        user = ibm_db.fetch_assoc(get_user)
        uid = user["ID"]

        get_password = ibm_db.exec_immediate(conn, f"SELECT password_hash FROM password WHERE user_id = {uid}")
        password = ibm_db.fetch_assoc(get_password)
        hashedpw = password["PASSWORD_HASH"]

        if bcrypt.checkpw(pword.encode('utf8'), hashedpw.encode('utf8')):
            cont = {"status": "ok", "cookie": sessionLogin(uid)}
        else:
            cont = {"status": "bad"}
        return jsonify(cont)
    return "Insufficient login data"



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
        return setCookie(sessid) #set cookie with new session id
    return None

def sessionLogin(uid):
    sess = findSess(uid)
    if sess:
        currentuser = finduser(sess["USER_ID"])
        if currentuser:
            return setCookie(sess["SESSION"]) #renew cookie for 1 more hour
        return "No user found"
    else:
        return addSession(uid)

def findSess(uid):
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
    expiration = datetime.datetime.now() + datetime.timedelta(hours=-4, seconds=60*60) #current EST + 1 hour
    c = SimpleCookie()
    c["session"] = sessid
    c["session"]["secure"] = True
    c["session"]["expires"] = expiration.strftime("%a, %d-%b-%Y %H:%M:%S EST")
    return c.output()

def generateSessId():
    return secrets.token_urlsafe(20)


@app.route('/logout')
def logout(uid=112):
    expiration = datetime.datetime.now() + datetime.timedelta(hours=-4, seconds=-60*60) #current EST - 1 hour
    c = SimpleCookie()
    c["session"] = ""
    c["session"]["expires"] =expiration.strftime("%a, %d-%b-%Y %H:%M:%S EST")
    
    ibm_db.exec_immediate(conn, f"DELETE from session WHERE USER_ID = {uid}")
    
    return c.output()