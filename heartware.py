"""
OPTIONAL ENV:
 - TIMEOUT, in seconds, default: 120
 - SPOKEPORT, default: 7181
 - BROADCAST_NEW_BEATS, default: '', broadcast first beats on (discovery/index) channel BROADCAST_NEW_BEATS
"""
"""
Run in development env:
export FLASK_ENV=development
export FLASK_APP=heartware.py
flask run
"""
from flask import Flask, Response, request # General flask, handle requests on the fly.

import sys # pathvalidate
from pathvalidate import ValidationError, validate_filename

from pkg.watchdog import reset_timer

### FLASK ###
app = Flask(__name__)

@app.route('/<string:userdata_heart_slug>', methods=['GET'])
def parse_request(userdata_heart_slug):
	try:  # https://pathvalidate.readthedocs.io/en/latest/pages/examples/validate.html
		validate_filename(userdata_heart_slug, platform="auto")
		heart_slug = userdata_heart_slug
	except ValidationError as e:
		return Response(f'Invalid slug: {e}', 400, mimetype='text/plain')

	try:
		err = reset_timer(heart_slug)
		if err: # tuple, 0:http code, 1:message
			return Response(err[1], err[0], mimetype='text/plain')
	except Exception as e:
		return Response(f'Beating heart failed: {e}', 500, mimetype='text/plain')

	return Response("Heartbeat received.", 200, mimetype='text/plain')
