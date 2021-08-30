# `http_reverse_heartbeat`
Relay remote heartbeats curling in.

## Github Actions Docker image
```sh
docker pull ghcr.io/jtagcat/http_reverse_heartbeat:1
```
Gunicorn listens on port `8000`. Mount `/data` for data persistancy.
## Usage
 - `/<heartbeat_slug>`

By the nature of no authentication, anyone can send heartbeats to a slug they know.

## Live instance
```sh
curl https://gtt.c7.ee/github_beat
```
