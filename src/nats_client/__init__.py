"""
NATS module: reusable client library for publish/subscribe communication.
"""
from .client import NatsClient, NatsConfig, MessageHandler

__all__ = ['NatsClient', 'NatsConfig', 'MessageHandler']
