from os import getenv
from threading import Timer, Thread

from asyncio import run as arun
import spoke


#### ENVIRONMENT ####
# no validation, panic towards admin is fine
TIMEOUT = int(getenv('TIMEOUT', '120'))
SPOKEPORT = int(getenv('SPOKEPORT', '7181'))
BROADCAST_NEW_BEATS = str(getenv('BROADCAST_NEW_BEATS', ''))


def start_spoke_server():
	spoke_server = spoke.pubsub.server.Server(conn_opts = {"port": SPOKEPORT})
	arun(spoke_server.run()) # error handling, inc bind inside spoke lib
Thread(target=start_spoke_server, name="Spoke Server").start()
print(f'Spoke started on 0.0.0.0: {SPOKEPORT}.')

timers = {}
alive = {}

def reset_timer(slug: str):
	if not slug in timers:
		alive[slug] = True
		spoke.publish(slug, 'first_beat', port=SPOKEPORT)
		if BROADCAST_NEW_BEATS:
			spoke.publish(BROADCAST_NEW_BEATS, 'first_beat', port=SPOKEPORT)
	else:
		if (alive[slug] == False):
			alive[slug] = True
			spoke.publish(slug, 'changeto_alive', port=SPOKEPORT)
		else:
			timers[slug].cancel()
			# there's no cleanup or resetting/restarting timers,
			# redefining the same-slugged timer hopefully releases the old thread

	# change status to dead on timeout
	timers[slug] = Timer(TIMEOUT, changeto_dead, [slug])
	timers[slug].start()

def changeto_dead(slug: str):
	alive[slug] = False
	spoke.publish(slug, 'changeto_dead', port=SPOKEPORT)
