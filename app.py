from flask import Flask, render_template, request, session, request, jsonify, make_response, redirect
from flask.ext.sqlalchemy import SQLAlchemy
from gevent.wsgi import WSGIServer
import os, random, datetime

app = Flask(__name__)
app.config['DEBUG'] = True
app.secret_key = 'SECRET KEY FOR CHERRYTEA SESSION'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['UPLOAD_FOLDER'] = os.path.abspath(os.path.join(os.path.dirname(__file__), 'static/prof_pic'))
app.config['PROF_PIC_STORAGE'] = '/static/prof_pic'

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

@app.route('/create/user', methods=['POST'])
def app_create_user():
	success = create_user(request.form['username'], request.form['password'],
			    request.form['user_type'], email=request.form['email'],
			    charity_number=request.form['charity_number']);
	return jsonify(success=success)

@app.route('/user/login', methods=['POST'])
def app_user_login():
	res = get_user_id(request.form['username'], request.form['password'])
	if res['success']:
		session['logged_in'] = True
		session['user_id'] = res['user_id']
		session['username'] = request.form['username']
	return jsonify(success=res['success'])

@app.route('/upload', methods=['POST'])
def app_upload():
	f = request.files['file']
	if f and is_allowed_file(f.filename):
		filename = session['username'] + '_' + str(random.randint(1,1000000)) + secure_filename(f.filename)
		f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
		ret = record_prof_pic(os.path.join(app.config['PROF_PIC_STORAGE'], filename))
		return jsonify(ret)
	return jsonify(success=False)

@app.route('/create/project')
def app_create_project():
	return render_template('create_project.html')

@app.route('/create/project/submit', methods=['POST'])
def app_create_project_submission():
	ret = create_project(session['user_id'], 
				   request.form.get('proj_name'), 
				   request.form.get('proj_desc'), 
				   request.form.get('location'), 
				   request.form.get('category'), 
				   request.form.get('donation_goal'), 
				   request.form.get('charity_org'), 
				   request.form.get('other_info'),
				   request.form.get('proj_pic'))
	return jsonify(ret)

@app.route('/project/<int:proj_id>')
def app_view_project(proj_id):
	info = get_project_profile(proj_id)
	info['followed'] = is_project_follower(proj_id, session['user_id'])
	info['broadcasts'] = get_recent_broadcasts(proj_id, 5)
	for b in info['broadcasts']:
		b['like'] = is_broadcast_liked(b['broadcast_id'], session['user_id'])
		b['replies'] = get_broadcast_reply(b['broadcast_id'])
	return render_template('project_profile.html', info=info)

@app.route('/project/<int:proj_id>/payment')
def app_view_project_payment(proj_id):
	session['payment'] = {}
	session['payment']['proj_id'] = proj_id
	info = get_project_profile(proj_id)
	return render_template('payment.html', info=info)


@app.route('/user')
def app_view_current_user():
	if session.get('user_id'):
		return redirect('/user/'+str(session['user_id']))
	return abort(404)

@app.route('/user/<int:user_id>')
def app_view_user(user_id):
	info = get_profile_info(session, user_id)
	return render_template('user_profile.html', info=info)

@app.route('/user_charity/<int:user_charity_id>')
def app_view_user_charity(user_charity_id):
	return render_template('user_charity_profile.html', user_charity_id=user_charity_id)

@app.route('/search_results/')
def app_view_search_results():
	return render_template('search_results.html', info={})

@app.route('/search_results/<search_term>')
def app_view_search_results_specified(search_term):
	info = {'search_term':search_term}
	return render_template('search_results.html', info=info)

@app.route('/update/user_profile/')
def app_update_profile():
	info = get_profile_info(session, session['user_id'])
	return render_template('update_profile.html', info=info)

@app.route('/update/user_profile/submit', methods=['POST'])
def app_update_profile_submission():
	# create profile
	params = {'first_name':request.form.get('first_name'),
			  'last_name':request.form.get('last_name'),
			  'bio':request.form.get('bio'),
			  'address':request.form.get('address'),
			  'advocate':request.form.get('advocate'),
			  'profile_pic_id':request.form.get('profile_pic_id')}
	
	if request.form.get('date_of_birth'):
		params['date_of_birth']=datetime.datetime.strptime(request.form.get('date_of_birth'), "%Y-%m-%d"),

	ret = update_user_profile(session['user_id'], params)
	return jsonify(ret)


@app.route('/record/donation', methods=['POST'])
def app_record_donation():
	# first iteration of payment method
	# transaction should be verifiable 
	# and should be done through SSL connection
	# this method does not implement those
	proj_id = request.form.get('proj_id')
	donation_amount = float(request.form.get('donation_amount'))
	paypal_id = request.form.get('paypal_id')
	if not session.get('payment', None) and proj_id != session['payment']['proj_id']:
		return jsonify(success=False)
	ret = record_donation(session['user_id'], proj_id, donation_amount, paypal_id)
	return jsonify(success=ret)

@app.route('/manage/project/<int:proj_id>')
def app_manage_project_by_id(proj_id):
	info = get_project_profile(proj_id)
	info['recent_donation'] = get_recent_donations(proj_id)
	info['recent_follower'] = get_recent_follower_info(proj_id)
	return render_template("manage_project.html", info=info)

@app.route('/project/<int:proj_id>/post/')
def app_manage_post(proj_id):
	info = get_project_profile(proj_id)
	return render_template('post.html', info=info)

@app.route('/ajax/recent_project', methods=['GET'])
def app_get_recent_projects():
	size = int(request.args.get('size', 3))
	offset = request.args.get('offset', None)
	return get_json_response(get_recent_projects(size, offset))

@app.route('/ajax/popular_project', methods=['GET'])
def app_get_popular_projects():
	size = int(request.args.get('size', 3))
	offset = request.args.get('offset', None)
	return get_json_response(get_popular_projects(size, offset))

@app.route('/ajax/search', methods=['GET'])
def app_search_project():
	search_term = request.args.get('search_term')
	size = int(request.args.get('size', 10))
	offset = int(request.args.get('offset', 0))
	return get_json_response(search_project(search_term, {'size':size, 'offset':offset}))
	
@app.route('/ajax/follow', methods=['POST'])
def app_follow_project():
	proj_id = request.form.get('proj_id')
	return jsonify(success=follow_project(session['user_id'], proj_id))

@app.route('/ajax/unfollow', methods=['POST'])
def app_unfollow_project():
	proj_id = request.form.get('proj_id')
	return jsonify(success=unfollow_project(session['user_id'], proj_id))

@app.route('/ajax/post', methods=['POST'])
def app_publish_project_post():
	proj_id = request.form.get('proj_id')
	title = request.form.get('title')
	content = request.form.get('entry')
	return jsonify(success=post_broadcast(proj_id, title, content))

@app.route('/post/reply', methods=['POST'])
def app_post_reply():
	content = request.form.get('content')
	broadcast_id = int(request.form.get('broadcast_id'))
	return jsonify(success=reply_broadcast(broadcast_id, session['user_id'], content))

@app.route('/post/like', methods=['POST'])
def app_post_like():
	broadcast_id = request.form.get('broadcast_id')
	return jsonify(success=like_broadcast(broadcast_id, session['user_id']))


@app.route('/post/unlike', methods=['POST'])
def app_post_unlike():
	broadcast_id = request.form.get('broadcast_id')
	return jsonify(success=unlike_broadcast(broadcast_id, session['user_id']))

@app.route('/update/project/<int:proj_id>')
def app_update_project(proj_id):
	info = get_project_profile(proj_id)
	return render_template('update_project.html', info=info)


@app.route('/update/project/submit', methods=['POST'])
def app_update_project_submission():
	ret = update_project(request.form.get('proj_id'), 
				   request.form.get('proj_name'), 
				   request.form.get('proj_desc'), 
				   request.form.get('location'), 
				   request.form.get('category'), 
				   request.form.get('donation_goal'), 
				   request.form.get('charity_org'), 
				   request.form.get('other_info'),
				   request.form.get('proj_pic'))
	return jsonify(ret)

@app.route('/dashboard')
def app_dashboard():
	info = get_owned_projects(session['user_id'])
	return render_template('dashboard.html',info=info)

@app.route('/ajax/donation_stats')
def app_donation_stats():
	proj_id = request.args.get('proj_id')
	return get_json_response(get_donation_statistics(proj_id))

@app.route('/ajax/notif')
def get_notification():
	if not session.get('user_id'):
		return get_json_response([])
	offset_id = request.args.get('offset_id', 0)
	return get_json_response(retrieve_notification(session['user_id'], offset_id))

@app.route('/ajax/notif/read')
def mark_read_notification():
	notif_id = request.args.get('notif_id')
	return jsonify(success=mark_notification_as_read(notif_id))

@app.route('/logout')
def app_logout():
	session.clear()
	return redirect('/')

# error handler
@app.errorhandler(404)
def page_not_found(e):
	return render_template('not_found.html')


# debugging routes
@app.route('/test_upload')
def test_upload():
	return render_template('test_upload.html')

@app.route('/clear_session')
def clear_session():
	session.clear();
	return make_response("Session cleared.")


if __name__ == '__main__':
	server = WSGIServer(('',5000),app)
	server.serve_forever()
	#app.run(host='0.0.0.0', debug=True)
