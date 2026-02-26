# NATS test repo — Laptop broker, Raspberry Pi client

This repository provides a minimal Python setup to test **NATS** communication between a laptop
(which hosts the broker) and a Raspberry Pi over Wi‑Fi. The original MQTT/Mosquitto code has
been adapted to use the asyncio‑based `nats-py` client library.

Files and directory structure
```
src/
  nats_client/    # Core NATS client library wrapper
    __init__.py
    client.py     # NatsClient, NatsConfig, MessageHandler classes
  examples/       # Example scripts (publisher + subscriber)
requirements.txt
README.md
```

Quick overview
- Laptop: install and run the NATS broker (`nats-server`). Use `publisher.py` to publish
  test messages.
- Raspberry Pi: run `subscriber.py` to receive messages from the laptop's broker.

Prerequisites
- On both machines: Python 3.8+ and pip.
- On the laptop (broker host): install the NATS server.

Install NATS server on Debian/Ubuntu (laptop):

```bash
# download latest release from https://github.com/nats-io/nats-server/releases
# or use your package manager if available; for example:
sudo apt update
sudo apt install -y nats-server
```

The server listens on port `4222` by default. Adjust firewall rules if necessary.

Python packages (both machines):

```bash
python3 -m pip install -r requirements.txt
```

How to run

- Start the broker on the laptop (you can also use `./scripts/run_local_broker.sh`):

```bash
nats-server -c nats_local.conf
```

- On the laptop (publisher): run the publisher pointing at the broker URL (LAN IP or
  `localhost` for local testing):

```bash
python3 src/examples/publisher.py --server nats://192.168.1.10:4222
```

- On the Raspberry Pi (subscriber): run the subscriber in a similar way:

```bash
python3 src/examples/subscriber.py --server nats://192.168.1.10:4222
```

What each file is for
- [src/nats_client/](src/nats_client/): core NATS library wrapper
  - [src/nats_client/__init__.py](src/nats_client/__init__.py): exports `NatsClient`, `NatsConfig`, `MessageHandler`
  - [src/nats_client/client.py](src/nats_client/client.py): small wrapper around `nats-py` with a synchronous
    convenience layer and callback hooks.
- [src/examples/](src/examples/): example scripts demonstrating publish/subscribe usage.

Explanation of the main Python imports used
- `nats.aio.client`: the official asyncio‑based NATS client library; used to connect, publish and
  subscribe to a NATS broker.
- `argparse`: simple CLI argument parsing (e.g. to pass `--server` URL).
- `asyncio` / `threading`: utilities used for running the event loop in a background thread so that
  example scripts can remain synchronous.
- `dataclasses`: convenient typed containers (for configuration).

Next steps
- Install the NATS server, install the Python requirements on both machines, then start the
  subscriber on the Pi and publisher on the laptop. The `run_local_broker.sh` script can be used
  to launch the broker with the provided `nats_local.conf` file.
