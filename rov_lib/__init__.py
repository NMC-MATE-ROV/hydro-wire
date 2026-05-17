"""rov-lib package - ROV communication and control library"""

__all__ = ["WebSocketCommandClient", "ROVManager", "start", "get_manager"]
__version__ = "0.0.1"

from .client import WebSocketCommandClient
from .manager import ROVManager, start, get_manager
