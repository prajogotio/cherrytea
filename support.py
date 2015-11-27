from dbapi import *
import json
from flask import Response

def jsondumpwrapper(obj):
	if hasattr(obj, 'isoformat'):
		return obj.isoformat()
	else:
		return None


def getJsonResponse(js):
	return Response(js, default=obj, mimetype='application/json')