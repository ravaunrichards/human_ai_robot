"""Modular conversation system with replaceable AI provider adapters."""

from .base import ConversationProvider, ConversationError, Message
from .echo_provider import EchoProvider
from .local_provider import LocalLLMProvider
from .online_provider import OnlineProvider
from .manager import ConversationManager

__all__ = [
    "ConversationProvider",
    "ConversationError",
    "Message",
    "EchoProvider",
    "LocalLLMProvider",
    "OnlineProvider",
    "ConversationManager",
]
