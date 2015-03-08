from flask import render_template, url_for, Flask, request, jsonify
from app import app
import hashlib
import RPi.GPIO as GPIO
import time
import sqlite3
from flask.ext.qrcode import QRcode

# @app.route('/')
# @app.route('/index')
# def index():
#     #door = {'status' : 'Locked'}
#     uuid_key = str(uuid.uuid4())
#     auth = hashlib.md5(uuid_key).hexdigest()
#     return render_template('index.html', title='Test', gen_code=auth)

# @app.route('/open')
# def buka():
#     door = {'status' : 'Open'} 
#     return render_template('opened.html', title='Open', door=door)

# @app.route('/generate')
# def generate():
#     return render_template('opened.html', title='Generate')

# @app.route('/auth/<secretcode>')
# def auth(secretcode):
#     return render_template('auth.html', secretcode)

#QRcode(app)

GPIO.setmode(GPIO.BCM)
GPIO.setup(25, GPIO.OUT)
#GPIO.output(25, GPIO.LOW)


@app.route('/')
def index():
	kode = c().execute("SELECT * FROM config").fetchone()[4]

	while true:
		if statusplain()=='locked':
   	        	GPIO.OUTPUT(25, GPIO.LOW)
        	if statusplain()=='unlocked':
                	GPIO.OUTPUT(25, GPIO.HIGH)

	return render_template('index.html', gen_code=kode)

@app.route('/unlocked')
def unlocked():
	return render_template('unlocked.html')

@app.route('/locked')
def locked():
	kode = c().execute("SELECT * FROM config").fetchone()[4]
	return render_template('locked.html', gen_code=kode)

@app.route('/locate')
def phone():
	long = c().execute("SELECT * FROM mediatrac").fetchone()[1]
	lat = c().execute("SELECT * FROM mediatrac").fetchone()[2]
	time = c().execute("SELECT * FROM mediatrac").fetchone()[3]

	return render_template('api.html',long=long,lat=lat,waktu=time)


@app.route('/open', methods=['POST'])
def open():
	conn = sqlite3.connect("qrlock.db")
	cursor = conn.cursor()
	kode = cursor.execute(""" SELECT * FROM config """).fetchone()[5]
	status = cursor.execute(""" SELECT * FROM config """).fetchone()[2]
	if status == '0':
		if request.form['txtScan'] == kode:
			cursor.execute("UPDATE config SET status=1 ")
			conn.commit()
			#conn.close()
			opendoor()
	return 'open'

@app.route('/lock', methods=['POST'])
def lock():
	conn = sqlite3.connect("qrlock.db")
	cursor = conn.cursor()
	if request.form['lock'] == hashlib.md5("lock").hexdigest():
		if cursor.execute(" SELECT * FROM config ").fetchone()[2] == '1':
			cursor.execute(""" UPDATE config SET status=0 """)
			waktu = time.strftime("%H:%M:%S")
			qr = hashlib.md5(waktu.encode('utf-8')).hexdigest()
			pin = cursor.execute(""" SELECT * FROM config """).fetchone()[3]
			kode = hashlib.md5(qr+pin).hexdigest()
			cursor.execute(""" UPDATE config SET qrcode=?, enc=? """, (qr, kode))
			conn.commit()
			#conn.close()
		closedoor()
	return 'lock'

@app.route('/enc')
def eee():
	return c().execute("SELECT * FROM config").fetchone()[5];

@app.route('/status')
def status():
	panto =  c().execute("SELECT * FROM config").fetchone()[2]
	if panto == '0':
		return jsonify({"emp_info":[{"id":"1","statusnya":"locked"}]})
	else:
		return jsonify({"emp_info":[{"id":"1","statusnya":"unlocked"}]})

@app.route('/statusplain')
def statusplain():
	panto = c().execute("SELECT * FROM config").fetchone()[2]
	if panto == '0':
		return 'locked'
	else:
		return 'unlocked'


@app.route('/apalah')
def apalah():
	a = 'adsad'
	b = 'lkjlkj'
	return a+b

@app.route('/install')
def install():
 	conn = sqlite3.connect("qrlock.db")
 	cursor = conn.cursor()
 	cursor.execute("""CREATE TABLE config(id integer, name text, status text, pin text, qrcode text, enc text)""")
 	cursor.execute(""" INSERT INTO config VALUES(1,'door1', '0', '1727','e8fe5cf9ac9de0789ad06c103105d723','6ade7c715a1a782a7e706e51baf4c4d2') """)	
 	cursor.execute(""" CREATE TABLE mediatrac(id int, long text, lat text, time text) """)
	cursor.execute(""" INSERT INTO mediatrac(id,long,lat,time) values(1,'-6.20','106.82','8-3-2015 8:43') """)
	conn.commit()

	#metadata = MetaData(db)
        #config = Table('config', metadata,
        #        Column('id', Integer, primary_key=True),
        #        Column('name', String),
        #        Column('status', String),
        #        Column('pin', String),
        #        Column('qrcode', String),
        #        Column('enc', String),
        #)
	#config.create()
	#a = hashlib.md5('Yuda Love Laode').hexdigest()
	#b = hashlib.md5(a+'1727').hexdigest()
	#config.insert().execute(name='door1', status=0, pin=1727, qrcode=a, enc=b)
#	return " Installed "

@app.route('/show')
def tampil():
	row = c().execute("SELECT * FROM config").fetchone()
	return row[2]

# Function

def c():
	conn = sqlite3.connect('qrlock.db')
	return conn	


def closedoor():
#	GPIO.setmode(GPIO.BCM)
#	GPIO.setup(25, GPIO.OUT)
	GPIO.OUTPUT(25, GPIO.LOW)
def opendoor():
#	GPIO.setmode(GPIO.BCM)
#	GPIO.setup(25, GPIO.OUT)
	GPIO.OUTPUT(25, GPIO.HIGH)
