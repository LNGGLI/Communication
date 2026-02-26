"""
Synchronous-friendly wrapper around the asyncio-based `nats-py` client.

This module provides:
- `NatsConfig`: small config dataclass
- `NatsClient`: wrapper around `nats.aio.client.Client` with background loop
- `MessageHandler`: example callback handler to override or extend

The native NATS Python library is async; the helper below runs an event
loop in a dedicated thread so that callers can use a simple synchronous
interface similar to the old MQTT version.
"""
from dataclasses import dataclass
from typing import Optional, List
import threading
import asyncio

from nats.aio.client import Client as NATS
from nats.aio.errors import ErrConnectionClosed, ErrTimeout, ErrNoServers


@dataclass
class NatsConfig:
    # list of server URLs (nats://host:port)
    servers: Optional[List[str]] = None
    # convenience field for a single server
    server: Optional[str] = None
    # connection timeout in seconds
    connect_timeout: float = 2.0


class MessageHandler:
    """Base handler: override methods to change behaviour."""

    async def on_connect(self, nc: NATS):
        print("Connected to NATS server")

    async def on_message(self, msg):
        print(f"Received message on {msg.subject}: {msg.data.decode()}")


class NatsClient:
    """Compact client with synchronous façade.

    Example:

        cfg = NatsConfig(server='nats://localhost:4222')
        client = NatsClient(cfg)
        client.connect()
        client.subscribe('foo')
        client.publish('foo', 'hello')
        client.close()
    """

    def __init__(self, config: NatsConfig, handler: Optional[MessageHandler] = None):
        self.config = config
        self.handler = handler or MessageHandler()
        self._nc = NATS()
        self._loop = asyncio.new_event_loop()
        self._thread = threading.Thread(target=self._run_loop, daemon=True)
        self._connected_event = threading.Event()

    def _run_loop(self):
        asyncio.set_event_loop(self._loop)
        self._loop.run_forever()

    def connect(self, timeout: Optional[float] = None):
        if timeout is None:
            timeout = self.config.connect_timeout
        if not self._thread.is_alive():
            self._thread.start()

        if self.config.servers:
            servers = self.config.servers
        elif self.config.server:
            servers = [self.config.server]
        else:
            servers = ["nats://127.0.0.1:4222"]

        async def do_connect():
            await self._nc.connect(servers=servers, timeout=timeout, loop=self._loop)
            await self.handler.on_connect(self._nc)
            self._connected_event.set()

        fut = asyncio.run_coroutine_threadsafe(do_connect(), self._loop)
        fut.result(timeout)

    def close(self):
        async def do_close():
            await self._nc.drain()
            await self._nc.close()
            self._loop.stop()

        fut = asyncio.run_coroutine_threadsafe(do_close(), self._loop)
        fut.result()
        self._thread.join()

    def publish(self, subject: str, payload: str):
        async def do_pub():
            await self._nc.publish(subject, payload.encode())

        asyncio.run_coroutine_threadsafe(do_pub(), self._loop)

    def subscribe(self, subject: str, queue: Optional[str] = None):
        async def cb(msg):
            await self.handler.on_message(msg)

        async def do_sub():
            await self._nc.subscribe(subject, queue=queue, cb=cb)

        asyncio.run_coroutine_threadsafe(do_sub(), self._loop)
