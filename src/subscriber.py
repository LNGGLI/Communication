"""Subscriber script

It connects to the NATS server and prints messages it receives.
"""
import argparse
import sys
import os

# Add parent directory to path so we can import from src.nats_client
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from nats_client import NatsClient, NatsConfig, MessageHandler


class PrintHandler(MessageHandler):
    async def on_message(self, msg):
        print(f"[subscriber] {msg.subject} -> {msg.data.decode()}")


def main():
    parser = argparse.ArgumentParser(description='Simple NATS subscriber')
    parser.add_argument('--server', required=True, help='NATS server URL')
    parser.add_argument('--subject', default='test', help='Subject to subscribe')
    args = parser.parse_args()

    cfg = NatsConfig(server=args.server)
    handler = PrintHandler()
    client = NatsClient(cfg, handler)
    client.connect()

    # subscribe after connecting so the handler sees incoming messages
    client.subscribe(args.subject)

    print(f"Subscribed to {args.subject} on server {args.server}. Ctrl-C to quit.")
    try:
        while True:
            pass
    except KeyboardInterrupt:
        print('Stopping subscriber')
    finally:
        client.close()


if __name__ == '__main__':
    main()
