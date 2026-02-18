"""Simple publisher script intended to run on the laptop (or any machine).

This script connects to the broker (default: pass --broker) and publishes a message every second.
"""
import argparse
import time
from dataclasses import dataclass
import sys
import os

# Add parent directory to path so we can import from src.mqtt
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from mqtt import MqttClient, MqttConfig


def main():
    parser = argparse.ArgumentParser(description='Simple MQTT publisher')
    parser.add_argument('--broker', required=True, help='Broker IP or hostname')
    parser.add_argument('--topic', default='test/topic', help='Topic to publish')
    parser.add_argument('--port', type=int, default=1883, help='Broker port')
    args = parser.parse_args()

    cfg = MqttConfig(broker=args.broker, port=args.port)
    client = MqttClient(cfg)
    client.connect()

    try:
        i = 0
        print(f"Publishing to broker {args.broker} on topic {args.topic}")
        while True:
            payload = f"hello from laptop #{i}"
            client.publish(args.topic, payload)
            print(f"Published: {payload}")
            i += 1
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopping publisher")
    finally:
        client.disconnect()


if __name__ == '__main__':
    main()
