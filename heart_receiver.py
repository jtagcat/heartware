"""
OPTIONAL ENV:
 - TIMEOUT, in seconds, default: 120
"""
"""
Run in development env:
export FLASK_ENV=development
export FLASK_APP=heart_receiver.py
flask run
"""

from flask import Flask, Response, request # General flask, handle requests on the fly.
from os import getenv

import sys # pathvalidate
from pathvalidate import ValidationError, validate_filename

from threading import Timer
import socketserver

### ENV Vars ###
TIMEOUT = int(getenv('TIMEOUT', '120'))

### FLASK ###
app = Flask(__name__)


@app.route('/<string:userdata_heart_slug>', methods=['GET'])
def parse_request(userdata_heart_slug):
	try:  # https://pathvalidate.readthedocs.io/en/latest/pages/examples/validate.html
		validate_filename(userdata_heart_slug, platform="auto")
		heart_slug = userdata_heart_slug
	except ValidationError as e:
		return Response(f'Invalid slug: {e}', 400, mimetype='text/plain')

#	try:
	reset_timer(heart_slug)
#	except Exception as e:
#		return Response(f'Beating heart failed: {e}', 500, mimetype='text/plain')

	return Response("Heartbeat received.", 200, mimetype='text/plain')

timers = {}
alive = {}

def reset_timer(slug: str):
	if not slug in timers:
		slug_newly_alive(slug)
	else:
		if (alive[slug] == False):
			slug_changestatus_alive(slug)
		else:
			timers[slug].cancel()
			# there's no cleanup or resetting/restarting timers,
			# redefining the same-slugged timer hopefully releases the old thread

	# change status to dead on timeout
	timers[slug] = Timer(TIMEOUT, now_changestatus_dead, [slug])
	timers[slug].start()

def slug_newly_alive(slug: str):
	alive[slug] = True
	print('newly alive: ' + slug)

def slug_changestatus_alive(slug: str):
	alive[slug] = True
	print('now alive: ' + slug)


def now_changestatus_dead(slug: str):
	alive[slug] = False
	print('now dead: ' + slug)