from flask import Flask, render_template, request, session, request, jsonify
from flask.ext.sqlalchemy import SQLAlchemy
from gevent.wsgi import WSGIServer

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/cherryteadb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)
db.session.autoflush = False
# import database api
from support import *


# Homepage
@app.route('/')
def index():
	return render_template('index.html')

@app.route('/register')
def register():
	return render_template('register.html')

@app.route('/create_user', methods=['POST'])
def app_create_user():
	success = create_user(request.form['username'], request.form['password'],
			    request.form['user_type'], email=request.form['email'],
			    charity_number=request.form['charity_number']);
	return jsonify(success=success)

if __name__ == '__main__':
	server = WSGIServer(('',5000),app)
	server.serve_forever()
	#app.run(host='0.0.0.0', debug=True)