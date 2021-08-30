# `heartware`
HTTP reverse heartbeat middleware service.  
Heartbeats may 'curl' the service, `hearware` sends `first_beat`/`changeto_alive`/`changeto_dead` messages to the spoke channels of slugs chosen by heartbeaters.

`spoke_heartbeat:{n}` is also sent out by the server, to all active slugs, every `TIMEOUT/2` seconds.  
(`spoke_heartbeat:60` indicates the signal is scheduled for every 60s)

## Github Actions Docker image
```sh
docker pull ghcr.io/jtagcat/http_reverse_heartbeat:1
```
Gunicorn listens on port `8000`, spoke on `7181`.

If set, environment value `BROADCAST_NEW_BEATS` defines the spoke channel on where to send new (since restart¹) heartbeat channels.  
This acts as a discovery channel for other channels.

¹ Make an issue if you need restart awareness.

## Usage and Live Instance
```sh
curl https://hw.c7.ee/github_beat
```

By the nature of no authentication, anyone can send heartbeats, and read  to a slug they know.

Subscribe with [pyspoke](https://gitlab.com/samflam/pyspoke):
```py
"Subscriber"
import asyncio
import spoke

async def handle_foo(msg):
    print(f"github_beat: {msg.body}")

async def main():
    client = spoke.pubsub.client.Client(conn_opts = {"host": "hw.c7.ee"})
    await client.run()
    await client.subscribe("github_beat", handle_foo)
    await spoke.wait()

asyncio.run(main())
```
