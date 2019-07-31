from server import app
from flask import render_template, Flask
import ibm_db

# app.config['DB2_DATABASE'] = 'BLUDB'
# app.config['DB2_HOSTNAME'] = 'dashdb-txn-sbox-yp-dal09-04.services.dal.bluemix.net'
# app.config['DB2_PORT'] = 50000
# app.config['DB2_PROTOCOL'] = 'TCPIP'
# app.config['DB2_USER'] = 'gqf91534'
# app.config['DB2_PASSWORD'] = 'n8rbtmpr-0nfphqs'

# db = DB2(app) #You forgot that

# cur = db.connection.cursor()

conn = ibm_db.connect('DATABASE=BLUDB;'
                     'HOSTNAME=dashdb-txn-sbox-yp-dal09-04.services.dal.bluemix.net;'  # 127.0.0.1 or localhost works if it's local
                     'PORT=50000;'
                     'PROTOCOL=TCPIP;'
                     'UID=gqf91534;'
                     'PWD=n8rbtmpr-0nfphqs;', '', '')

@app.route("/api/get_all")
def get_all():
    if conn:
        return "Conncected to DB"
    return "not connected"
    # return cur.execute("SELECT * FROM user")