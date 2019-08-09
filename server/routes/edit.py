from server import app
from flask import render_template, Flask, jsonify, request
import ibm_db
import json
from flask_cors import CORS

import server.services.generate_password as passw
import server.services.user_service as user_s
# from server.services.generate_password import random_password as random_pass

CORS(app, supports_credentials=True)

@app.route("/edit", methods=["POST", "GET"])
def edit_user():
    conn = passw.connect() # Connect to database
    data = passw.getEditJSON() # Get JSON
    # return jsonify({"data": data})

    cont = dict()
    if request.method == "POST":
        # sql = "UPDATE userinternbio ON user.id = internbio.user_id SET "
        for _key, _dat in data.items():
            for key, dat in _dat.items():
                print(str(_key) + "-" + str(key) + " : " + str(dat))
            # if key != "USER_ID":
            #     if dat != None:
            #         sql += " {}={},".format(key, dat)

        # sql = sql[:-1] #remove last comma

        # sql += " WHERE user.id = {}".format(data["USER_ID"])

        # print(sql)
        # ibm_db.exec_immediate(conn, sql)

    ibm_db.close(conn) # CLose Connection
    return cont