from server import app
from flask import render_template, Flask, jsonify, request
import ibm_db
import json
from flask_cors import CORS

import server.services.generate_password as passw
# from server.services.generate_password import random_password as random_pass

CORS(app)


# Functions
def get_maxID(conn=None):

    if not conn: # Exit
        return {"data":{ 
            "error": "Not connected to the database",
            },
            "status": "Fail",
            "id": -1
        }

    cont = dict()
    try:
        # "SELECT USER.ID, USER.NAME, USER.EMAIL, USER.PHONENUMBER, EMPLOYEETYPE.TYPE, SITELOCATION.SITE  FROM ((USER INNER JOIN EMPLOYEETYPE ON USER.EMPLOYEETYPE_ID = EMPLOYEETYPE.ID) INNER JOIN SITELOCATION ON USER.SITELOCATION_ID = SITELOCATION.ID)"
        sql = "Select user.id, user.name, user.email, user.phonenumber, employeetype.type, sitelocation.site from  (( USER INNER JOIN EMPLOYEETYPE ON USER.EMPLOYEETYPE_ID = EMPLOYEETYPE.ID) INNER JOIN SITELOCATION ON USER.SITELOCATION_ID = SITELOCATION.ID) where USER.id = (Select Max(id) from user)"
        stmt = ibm_db.exec_immediate(conn, sql)
        result = ibm_db.fetch_assoc(stmt)
        cont = {"data": {
            "error": ibm_db.stmt_errormsg(),
            },
            "status": "ok",
            "id": result["ID"]
        }
    except:
        cont = {"data": {
            "error": ibm_db.stmt_errormsg(),
            },
            "status": "bad",
            "id": -1
        }
    finally:
        return cont

#End of Functions


@app.route('/test/test', methods=['POST', 'GET', 'DELETE'])
def test():
    conn = passw.connect()


    user = get_maxID(conn)
    stmt_1 = ibm_db.exec_immediate(conn, "SELECT * FROM USER")

    cont = passw.content(user=user["id"], err=ibm_db.stmt_errormsg(), status="ok")
    return jsonify(cont)

# return passw.random_password()


@app.route('/delete=<user_id>', methods=['POST', 'GET', 'DELETE'])
def user(user_id):
    #Connect To the database
    conn = passw.connect()

    cont = dict()

    #Make SQL queries
    sql_delete_user = "DELETE FROM user WHERE id={0}".format(user_id)
    sql_delete_user_bio = "DELETE FROM internbio WHERE user_id={}".format(
        user_id)
    sql_detele_password = "DELETE FROM password WHERE user_id={}".format(
        user_id)

    #Try to execute SQL 
    #Fails: Return status bad
    try:
        if request.method == 'DELETE':
            cont = {"status": "ok"}
            stmt_1 = ibm_db.exec_immediate(conn, sql_delete_user)
            stmt_2 = ibm_db.exec_immediate(conn, sql_delete_user_bio)
            stmt_3 = ibm_db.exec_immediate(conn, sql_detele_password)
    except:
        cont = {"status": "bad", "error": ibm_db.stmt_errormsg()}
        ibm_db.rollback(conn)
    finally:
        ibm_db.close(conn)
        return jsonify(cont)

    # Not connected Should Render Template "No Access to Database"


""" ADDING NEW USER"""
@app.route('/add', methods=['POST', 'GET'])
def add_user():
    #Get JSON
    data = request.get_json()

    #Connect To database
    conn = passw.connect()

    if conn:
        print("Connected")
    else:
        print("Not connected")

    #Store JSON in Dictionary (easy use)
    store_data = {
        "name": data["data"]["user"]["NAME"],
        "email": data["data"]["user"]["EMAIL"],
        "phone_number": data["data"]["user"]["PHONENUMBER"],
        "employeeType_id": data["data"]["user"]["EMPLOYEETYPE_ID"],
        "siteLocation_id": data["data"]["user"]["SITELOCATION_ID"],
        "password": passw.random_password()
    }

    #Make SQL Queries
    sql_add_user = "INSERT INTO user (name, email, phonenumber, employeeType_id, siteLocation_id) VALUES (?, ?, ?, ?, ?)"
    sql_add_pass = "INSERT INTO password (user_id, password_hash) VALUES (?, ?)"
    sql_add_bio = "INSERT INTO internbio (user_id, position) VALUES (?, ?)"
    
    #Prepare sql statement
    stmt_user = ibm_db.prepare(conn, sql_add_user)
    stmt_pass = ibm_db.prepare(conn, sql_add_pass)
    stmt_bio  = ibm_db.prepare(conn, sql_add_bio)

    cont = dict()

    #Try to Execute SQL queries, if so return json with user_id and ibm_db error
    #Else Return json with user_id,
    try:
        if request.method == 'POST':
            #ADDING TO USER TABLE
            params_user = store_data["name"], store_data["email"], store_data["phone_number"], store_data["employeeType_id"], store_data["siteLocation_id"]
            ibm_db.execute(stmt_user, params_user)

            #ADDING TO PASSWORD TABLE
            last_user = get_maxID(conn)
            params = last_user["id"], store_data["password"]
            ibm_db.execute(stmt_pass, params)

            #ADDING TO INTERNBIO TABLE
            params_1 = last_user["id"], "Software Engineer"
            ibm_db.execute(stmt_bio, params_1)
            cont = passw.content(user=last_user["id"], status="ok")
    except:
        cont = passw.content(user=None, err=ibm_db.stmt_errormsg(), status="bad")
        ibm_db.rollback(conn)
    finally:
        ibm_db.close(conn)
        return jsonify(cont)
