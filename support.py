from dbapi import *
import json
from flask import Response, send_file
from werkzeug import secure_filename

ALLOWED_EXTENSIONS = set(['jpeg', 'jpg', 'png', 'pdf', 'txt'])

def jsondumpwrapper(obj):
	if hasattr(obj, 'isoformat'):
		return obj.isoformat()
	else:
		return None


def getJsonResponse(js):
	return Response(getJson(js), mimetype='application/json')

def getJson(js):
	return json.dumps(js, default=jsondumpwrapper);

def get_user_id(username, password):
	try:
		u = User.query.filter(User.username==username)\
					  .filter(User.password==password)\
					  .first()
		if u:
			return {'success':True,
					'user_id':u.user_id}
		return {'success':False}
	except:
		return {'success':False}

def is_allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def get_profile_info(session, user_id):
	info = {}
	info['user_id'] = user_id
	info['username'] = get_username(user_id)
	info['join_date'] = get_join_date(user_id)
	info['num_of_backed_projects'] = get_num_of_backed_projects(user_id)
	info['recently_backed_projects'] = getJson(get_recently_backed_projects(user_id))
	info['membership'] = 'Private Individual' if get_membership(user_id) == User.USER_TYPE_INDIVIDUAL else "Charitable Organisation"
	info['profile_owner'] = user_id == session.get('user_id')
	info['profile'] = get_user_profile(user_id)
	return info
