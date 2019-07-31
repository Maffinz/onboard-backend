from server import app
from flask import render_template, Flask
# from flask_db2 import DB2
import ibm_db

# app.config['DB2_DATABASE'] = 'BLUDB'
# app.config['DB2_HOSTNAME'] = 'dashdb-txn-sbox-yp-dal09-04.services.dal.bluemix.net'
# app.config['DB2_PORT'] = 50000
# app.config['DB2_PROTOCOL'] = 'TCPIP'
# app.config['DB2_USER'] = 'gqf91534'
# app.config['DB2_PASSWORD'] = 'n8rbtmpr-0nfphqs'

# db = DB2(app) #You forgot that

# cur = db.connection.cursor()

@app.route("/api/get_all")
def get_all():
    return "api/get_all"
    # return cur.execute("SELECT * FROM user")