from flask import Flask, render_template, request, session, request, jsonify, make_response
from flask.ext.sqlalchemy import SQLAlchemy
from gevent.wsgi import WSGIServer
import os, random

app = Flask(__name__)
app.config['DEBUG'] = True
app.secret_key = 'SECRET KEY FOR CHERRYTEA SESSION'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cherryteadb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['UPLOAD_FOLDER'] = os.path.abspath(os.path.join(os.path.dirname(__file__), 'static/prof_pic'))

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

@app.route('/login')
def login():
	return render_template('login.html')

@app.route('/create_user', methods=['POST'])
def app_create_user():
	success = create_user(request.form['username'], request.form['password'],
			    request.form['user_type'], email=request.form['email'],
			    charity_number=request.form['charity_number']);
	return jsonify(success=success)

@app.route('/user_login', methods=['POST'])
def app_user_login():
	res = get_user_id(request.form['username'], request.form['password'])
	if res['success']:
		session['user_id'] = res['user_id']
		session['username'] = request.form['username']
	return jsonify(success=res['success'])

@app.route('/upload', methods=['POST'])
def app_upload():
	f = request.files['file']
	if f and is_allowed_file(f.filename):
		filename = session['username'] + '_' + str(random.randint(1,1000000)) + secure_filename(f.filename)
		f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
		ret = record_prof_pic(os.path.join(app.config['UPLOAD_FOLDER'], filename))
		return jsonify(ret)
	return jsonify(success=False)

@app.route('/create_project')
def app_create_project():
	return render_template('create_project.html')

@app.route('/create_project_submission', methods=['POST'])
def app_create_project_submission():
	ret = create_project(session['user_id'], 
				   request.form.get('proj_name'), 
				   request.form.get('proj_desc'), 
				   request.form.get('location'), 
				   request.form.get('category'), 
				   request.form.get('donation_goal'), 
				   request.form.get('charity_org'), 
				   request.form.get('proj_pic'))
	return jsonify(ret)

@app.route('/project/<int:proj_id>')
def app_view_project(proj_id):
	return render_template('project_profile.html', proj_id=proj_id)

@app.route('/project/<int:proj_id>/payment')
def app_view_project_payment(proj_id):
	return render_template('payment.html', proj_id=proj_id)

@app.route('/user/<int:user_id>')
def app_view_user(user_id):
	return render_template('user_profile.html', user_id=user_id)

@app.route('/user_charity/<int:user_charity_id>')
def app_view_user_charity(user_charity_id):
	return render_template('user_charity_profile.html', user_charity_id=user_charity_id)

@app.route('/search_results')
def app_view_search_results():
	return render_template('search_results.html')


@app.route('/test_upload')
def test_upload():
	return render_template('test_upload.html')

if __name__ == '__main__':
	server = WSGIServer(('',5000),app)
	server.serve_forever()
	#app.run(host='0.0.0.0', debug=True)
