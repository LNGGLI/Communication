"""Simple publisher script intended to run on the laptop (or any machine).

This script connects to the NATS server (default: pass --server URL) and publishes
a message every second.
"""
import argparse
import time
import sys
import os

# Add parent directory to path so we can import from src.nats_client
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from nats_client import NatsClient, NatsConfig


def main():
    parser = argparse.ArgumentParser(description='Simple NATS publisher')
    parser.add_argument('--server', required=True, help='NATS server URL (nats://host:port)')
    parser.add_argument('--subject', default='test', help='Subject to publish')
    args = parser.parse_args()

    cfg = NatsConfig(server=args.server)
    client = NatsClient(cfg)
    client.connect()

    try:
        i = 0
        print(f"Publishing to server {args.server} on subject {args.subject}")
        while True:
            payload = f"hello from laptop #{i}"
            client.publish(args.subject, payload)
            print(f"Published: {payload}")
            i += 1
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopping publisher")
    finally:
        client.close()


if __name__ == '__main__':
    main()
