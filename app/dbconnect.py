from flask import Flask
from flaskext.mysql import MySQL

mysql = MySQL()
app = Flask(__name__)
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'qwerty123'
app.config['MYSQL_DATABASE_DB'] = 'QRData'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)
 
if __name__ == "__main__":
    app.run()

@app.route("/Authenticate")
def Authenticate():
    username = request.args.get('Name')
    password = request.args.get('Value')
    cursor = mysql.connect().cursor()
    cursor.execute("SELECT * from data where Name='" + name + "' and Value='" + value + "'")
    data = cursor.fetchone()
    if data is None:
     return "Username or Password is wrong"
    else:
     return "Logged in successfully"
