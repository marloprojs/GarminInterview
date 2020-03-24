from resource import *
import flask
from flask import request, jsonify

app = flask.Flask(__name__)
app.config["DEBUG"] = True

token = getToken()

@app.route('/', methods=['GET'])
def home():
	return '''<h1>Distant Reading Archive</h1>
<p>A prototype API for distant reading of science fiction novels.</p>'''


# A route to return all of the available entries in our catalog.
@app.route('/compositeUsers/<path:userId>', methods=['GET'])
def cardFilter(userId):
	ccState = ""
	deviceState = ""
	j = makeJsonObjects(token, userId, ccState, deviceState)
	return jsonify(j)
		
	if('creditCardState' in request.args):
		ccState = request.args['creditCardState']
		j = makeJsonObjects(token, userId, ccState, "")
		return jsonify(j)
	elif('deviceState' in request.args):
		deviceState = request.args['deviceState']
		j = makeJsonObjects(token, userId, "", deviceState)
		return jsonify(j)

	#j = makeJsonObjects(token, userId, ccState, deviceState)
	#return jsonify(j)	

app.run()