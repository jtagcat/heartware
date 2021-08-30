"""
OPTIONAL ENV:
 - DATADIR
"""
"""
Run in development env:
export FLASK_ENV=development
export FLASK_APP=heart_receiver.py
flask run
"""

### ENV Vars ###
from flask import Flask, Response, request # General flask, and the handle requests on the fly thing.
from os import getenv, path
import requests
import time
import sys # pathvalidate
from pathvalidate import ValidationError, validate_filename

DATADIR = getenv('DATADIR','/data')

### FLASK ###
app = Flask(__name__)

@app.route('/<string:userdata_heart_slug>', methods=['GET'])
def parse_request(userdata_heart_slug):
	try: # https://pathvalidate.readthedocs.io/en/latest/pages/examples/validate.html
		validate_filename(userdata_heart_slug, platform="auto")
	except ValidationError as e:
		return Response(f'Invalid slug: {e}', 400, mimetype='text/plain')

	try: # writing to file instead of memory for long-time storage / recovery, os hopefully optimizes this
		textfile = open(path.join(DATADIR, userdata_heart_slug), "w")
		textfile.write(str(int(time.time()))) # write epoch, str for write format, int to get 1630292434 from 1630292434.4241803
		textfile.close()
	except Exception as e:
		return Response(f'Storing heartbeat failed: {e}', 500, mimetype='text/plain')

	return Response("Heartbeat received.", 200, mimetype='text/plain')
