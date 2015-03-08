#!flask/bin/python
from app import app
#from app import dbconnect
app.run(host="raspberrypi.mshome.net", debug=True)
