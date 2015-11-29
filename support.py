from dbapi import *
import json
from flask import Response
from werkzeug import secure_filename

ALLOWED_EXTENSIONS = set(['jpeg', 'jpg', 'png', 'pdf', 'txt'])

def jsondumpwrapper(obj):
	if hasattr(obj, 'isoformat'):
		return obj.isoformat()
	else:
		return None


def getJsonResponse(js):
	return Response(js, default=obj, mimetype='application/json')



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