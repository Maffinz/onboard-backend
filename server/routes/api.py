from server import app
from flask import render_template, Flask

# import ibm_db

# conn = ibm_db.connect(DATABASE="bludb", HOSTNAME = "dashdb-txn-sbox-yp-dal09-04.services.dal.bluemix.net", 
# PORT = 5000, PROTOCOL = "TCPIP", USER ="gqf91534", PASSWORD = "n8rbtmpr-0nfphqs")

# import ibm_db

# app.config['DB2_DATABASE'] = 'bludb'
# app.config['DB2_HOSTNAME'] = 'dashdb-txn-sbox-yp-dal09-04.services.dal.bluemix.net'
# app.config['DB2_PORT'] = 50000
# app.config['DB2_PROTOCOL'] = 'TCPIP'
# app.config['DB2_USER'] = 'gqf91534'
# app.config['DB2_PASSWORD'] = 'n8rbtmpr-0nfphqs'

#db = DB2(app) #You forgot that
#cur = db.connection.cursor()

@app.route("/api/get_all")
def get_all():
    return "api/get_all"
    # return cur.execute("SELECT * FROM user")