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

### Environment

 - `BROADCAST_NEW_BEATS`, default empty. If set, all `first_beat` messages will be broadcasted also to the channel `BROADCAST_NEW_BEATS`. This acts as a discovery channel for other channels.
 - `TIMEOUT`, default `120`, in seconds. Time to wait since last beat till death is announced (`changeto_dead`).
 - `SPOKEPORT`, default `7181`. Port on which the embedded `pyspoke` spoke server is exposed to.

¹ Make an issue if you need restart awareness.

## Usage and Live Instance
```sh
curl https://hw.c7.ee/github_beat
```

By the nature of no authentication, anyone can send heartbeats, and read to a slug they know.

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

### Spoke messages reference
Please reserve `:` as the seperator for additional info in messages.

 - `first_beat` — sent on first heartbeat received on the channel (since the server started). This is the first `changeto_alive` the server has recieved. If this is recieved outside of the `BROADCAST_NEW_BEATS` channel, it's likely that heartware (spoke server) restarted, losing it's memory of slugs.
 - `spoke_heartbeat` — after the first heartbeat, sent out regularly (currently implemented to be half of `TIMEOUT`).
   - `:n` (`spoke_heartbeat:60`) — period, where n, in seconds, the heartbeat is sent out. (Heartbeat is sent out every 60 seconds.)
 - `changeto_dead` — No heartbeat recieved within `TIMEOUT` seconds. Target assumed dead.
 - `changeto_alive` — Heartbeat was recieved on a dead target. Target assumed to be back alive.
