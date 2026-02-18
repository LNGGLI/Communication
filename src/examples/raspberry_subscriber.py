"""Subscriber script intended to run on the Raspberry Pi.

It connects to the laptop broker and prints messages it receives.
"""
import argparse
import sys
import os

# Add parent directory to path so we can import from src.mqtt
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from mqtt import MqttClient, MqttConfig, MessageHandler


class PrintHandler(MessageHandler):
    def on_connect(self, client, userdata, flags, rc):
        super().on_connect(client, userdata, flags, rc)
        # subscribe once connected
        client.subscribe('test/topic')

    def on_message(self, client, userdata, msg):
        print(f"[subscriber] {msg.topic} -> {msg.payload.decode()}")


def main():
    parser = argparse.ArgumentParser(description='Simple MQTT subscriber')
    parser.add_argument('--broker', required=True, help='Broker IP or hostname')
    parser.add_argument('--topic', default='test/topic', help='Topic to subscribe')
    parser.add_argument('--port', type=int, default=1883, help='Broker port')
    args = parser.parse_args()

    cfg = MqttConfig(broker=args.broker, port=args.port)
    handler = PrintHandler()
    client = MqttClient(cfg, handler)
    client.connect()

    print(f"Subscribed to {args.topic} on broker {args.broker}. Ctrl-C to quit.")
    try:
        # Keep the program alive; callbacks run in background loop
        while True:
            pass
    except KeyboardInterrupt:
        print('Stopping subscriber')
    finally:
        client.disconnect()


if __name__ == '__main__':
    main()
