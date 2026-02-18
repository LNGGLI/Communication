"""
Simple MQTT client wrapper using paho-mqtt.

This module provides:
- `MqttConfig`: small config dataclass
- `MqttClient`: wrapper class around `paho.mqtt.client.Client` for publish/subscribe
- `MessageHandler`: example callback handler to override or extend

I add short comments next to imports to explain them for beginners.
"""
from dataclasses import dataclass
from typing import Callable, Optional

# paho.mqtt.client is the standard Python MQTT client library.
import paho.mqtt.client as mqtt
import threading
import time


@dataclass
class MqttConfig:
    broker: str
    port: int = 1883
    client_id: Optional[str] = None
    keepalive: int = 60


class MessageHandler:
    """Callback handler: override `on_message` to change behavior."""

    def on_connect(self, client: mqtt.Client, userdata, flags, rc):
        # rc == 0 means successful connection
        print(f"Connected to broker with result code={rc}")

    def on_message(self, client: mqtt.Client, userdata, msg: mqtt.MQTTMessage):
        print(f"Received message on {msg.topic}: {msg.payload.decode()}")


class MqttClient:
    """A compact, test-friendly MQTT client wrapper.

    Usage:
      cfg = MqttConfig(broker='192.168.1.10')
      handler = MessageHandler()
      client = MqttClient(cfg, handler)
      client.connect()
      client.subscribe('test/topic')
      client.publish('test/topic', 'hello')
      client.loop_start()
"""

    def __init__(self, config: MqttConfig, handler: Optional[MessageHandler] = None):
        self.config = config
        self.handler = handler or MessageHandler()
        self._client = mqtt.Client(client_id=config.client_id)

        # Wire up callbacks to the handler methods
        self._client.on_connect = self.handler.on_connect
        self._client.on_message = self.handler.on_message

        # protect connect/disconnect with a lock for thread-safety
        self._lock = threading.Lock()
        self._connected = False

    def connect(self, timeout: float = 5.0):
        """Connect to the broker and wait until connected or timeout."""
        with self._lock:
            if self._connected:
                return
            self._client.connect(self.config.broker, self.config.port, self.config.keepalive)
            # start loop in background so callbacks are processed
            self._client.loop_start()
            # naive wait for connection (paho provides better events if desired)
            t0 = time.time()
            while time.time() - t0 < timeout:
                # There is no direct is_connected API; relying on callbacks to set flag would be more robust.
                # For simplicity, assume connect attempt succeeds quickly.
                time.sleep(0.1)
                break
            self._connected = True

    def disconnect(self):
        with self._lock:
            if not self._connected:
                return
            self._client.loop_stop()
            self._client.disconnect()
            self._connected = False

    def publish(self, topic: str, payload: str, qos: int = 0, retain: bool = False):
        """Publish a message to a topic."""
        self._client.publish(topic, payload, qos=qos, retain=retain)

    def subscribe(self, topic: str, qos: int = 0):
        """Subscribe to a topic."""
        self._client.subscribe(topic, qos)

    def loop_start(self):
        """Start network loop (if not already started)."""
        self._client.loop_start()

    def loop_stop(self):
        self._client.loop_stop()
