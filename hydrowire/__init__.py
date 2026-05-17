"""hydrowire package - HydroWire communication and control library"""

__all__ = ["WebSocketCommandClient", "HydroWireManager", "start", "get_manager"]
__version__ = "0.0.1"

from .client import WebSocketCommandClient
from .manager import HydroWireManager, start, get_manager

