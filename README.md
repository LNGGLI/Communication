# MQTT test repo — Laptop broker, Raspberry Pi client

This repository provides a minimal Python setup to test MQTT communication between a laptop (which will host the broker) and a Raspberry Pi over Wi‑Fi.

Files and directory structure
```
src/
  mqtt/           # Core MQTT library
    __init__.py
    client.py     # MqttClient, MqttConfig, MessageHandler classes
  examples/       # Example scripts
    laptop_publisher.py      # Publisher (run on laptop/test machine)
    raspberry_subscriber.py  # Subscriber (run on Raspberry Pi)
requirements.txt
README.md
```

Quick overview
- Laptop: install and run the MQTT broker (Mosquitto). Run `laptop_publisher.py` to publish test messages.
- Raspberry Pi: run `raspberry_subscriber.py` to receive messages from the laptop's broker.

Prerequisites
- On both machines: Python 3.8+ and pip.
- On the laptop (broker host): install Mosquitto.

Install Mosquitto on Debian/Ubuntu (laptop):

```bash
sudo apt update
sudo apt install -y mosquitto mosquitto-clients
sudo systemctl enable --now mosquitto
```

If the laptop runs a firewall, allow port 1883/TCP in the local network.

Python packages (both machines):

```bash
python3 -m pip install -r requirements.txt
```

How to run

- Start the broker on the laptop (Mosquitto usually runs automatically after install). Verify it:

```bash
mosquitto_sub -h localhost -t test/topic -v &
mosquitto_pub -h localhost -t test/topic -m "hello" 
```

- On the laptop (publisher): run the publisher pointing at the laptop's LAN IP (or `localhost` to test locally):

```bash
python3 src/examples/laptop_publisher.py --broker 192.168.1.10
```

- On the Raspberry Pi (subscriber): run the subscriber, pointing at the laptop's IP:

```bash
python3 src/examples/raspberry_subscriber.py --broker 192.168.1.10
```

What each file is for
- [src/mqtt/](src/mqtt/): core MQTT library
  - [src/mqtt/__init__.py](src/mqtt/__init__.py): exports `MqttClient`, `MqttConfig`, `MessageHandler`
  - [src/mqtt/client.py](src/mqtt/client.py): small, well-documented class wrapper around `paho-mqtt` with helpful callbacks.
- [src/examples/](src/examples/): example scripts
  - [src/examples/laptop_publisher.py](src/examples/laptop_publisher.py): publisher that sends periodic test messages (run on laptop or test machine).
  - [src/examples/raspberry_subscriber.py](src/examples/raspberry_subscriber.py): subscribes and prints received messages (intended for Raspberry Pi).

Explanation of the main Python imports used
- `paho.mqtt.client`: the standard Python MQTT client library — used to connect, publish and subscribe to an MQTT broker.
- `argparse`: simple CLI argument parsing (e.g., to pass `--broker` IP).
- `time` / `threading`: small utilities used for sleeping and running the network loop in the background.
- `dataclasses`: convenient typed containers (for configuration).

Next steps
- Run the install commands above on both machines, then start the subscriber on the Pi and publisher on the laptop. If you want, I can also add an example that uses TLS or credentials.
