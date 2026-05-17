"""ROV Library Manager - Main entry point for library initialization and control."""
import asyncio
from typing import Optional, Dict, Any, Callable
from .client import WebSocketCommandClient


class ROVManager:
    """Main manager class for ROV communication and application control.

    Handles WebSocket connection to ROV, command routing to devices,
    and integration with optional GUI components.
    """

    def __init__(self, rov_uri: str, timeout: float = 10.0):
        """Initialize ROV Manager.

        Args:
            rov_uri: WebSocket URI for ROV (e.g., "ws://localhost:8000")
            timeout: Command timeout in seconds
        """
        self.rov_uri = rov_uri
        self.timeout = timeout
        self.client: Optional[WebSocketCommandClient] = None
        self._running = False
        self._gui_app = None
        self._command_handlers: Dict[str, Callable] = {}

    async def initialize(self) -> None:
        """Initialize connection to ROV."""
        self.client = WebSocketCommandClient(self.rov_uri, timeout=self.timeout)
        await self.client.connect()
        self._running = True
        print(f"ROV Manager initialized. Connected to {self.rov_uri}")

    async def close(self) -> None:
        """Close ROV connection."""
        if self.client:
            await self.client.close()
        self._running = False
        print("ROV Manager closed")

    async def send_command(
        self,
        device_id: str,
        command: Dict[str, Any],
        expect_response: bool = False
    ) -> Optional[Dict[str, Any]]:
        """Send a command to a specific device on the ROV.

        Args:
            device_id: Target device ID (e.g., "arm_1", "camera_main")
            command: Command dictionary with action and parameters
            expect_response: Whether to wait for response

        Returns:
            Response dict if expect_response=True, otherwise None

        Example:
            response = await manager.send_command(
                device_id="arm_1",
                command={"action": "move", "position": 45},
                expect_response=True
            )
        """
        if not self._running or not self.client:
            raise RuntimeError("ROV Manager not initialized. Call initialize() first.")

        return await self.client.send_command(device_id, command, expect_response)

    def register_command_handler(self, command_type: str, handler: Callable) -> None:
        """Register a handler for a specific command type.

        Args:
            command_type: Command type identifier
            handler: Async callable that processes the command
        """
        self._command_handlers[command_type] = handler

    def attach_gui(self, gui_app: Any) -> None:
        """Attach a GUI application instance.

        The GUI app will be configurable from the main application
        and can communicate back through registered callbacks.

        Args:
            gui_app: GUI application instance
        """
        self._gui_app = gui_app
        print("GUI application attached to ROV Manager")

    async def start(self, gui_enabled: bool = False, **gui_config) -> None:
        """Start the ROV library - initialize communication and optionally start GUI.

        Args:
            gui_enabled: Whether to start the GUI application
            **gui_config: Configuration options for the GUI

        Example:
            manager = ROVManager("ws://localhost:8000")
            await manager.start(gui_enabled=True, theme="dark")
        """
        await self.initialize()

        if gui_enabled:
            await self._start_gui(**gui_config)

    async def _start_gui(self, **config) -> None:
        """Start GUI application with provided configuration.

        Args:
            **config: GUI configuration options
        """
        if self._gui_app:
            print(f"Starting GUI with config: {config}")
            # GUI initialization will be implemented here
            # The GUI will have access to send_command through the manager
        else:
            print("No GUI app attached. Skipping GUI startup.")

    async def run(self, gui_enabled: bool = False, **gui_config) -> None:
        """Run the ROV Manager (blocking).

        Args:
            gui_enabled: Whether to start the GUI application
            **gui_config: Configuration options for the GUI
        """
        try:
            await self.start(gui_enabled=gui_enabled, **gui_config)
            # Keep running until interrupted
            while self._running:
                await asyncio.sleep(1)
        except KeyboardInterrupt:
            print("\nShutdown signal received")
        finally:
            await self.close()


# Global manager instance (optional convenience interface)
_manager: Optional[ROVManager] = None


async def start(rov_uri: str, gui_enabled: bool = False, **gui_config) -> ROVManager:
    """Start the ROV library with default configuration.

    Args:
        rov_uri: WebSocket URI for ROV (e.g., "ws://localhost:8000")
        gui_enabled: Whether to start the GUI application
        **gui_config: Configuration options for the GUI

    Returns:
        ROVManager instance

    Example:
        manager = await start("ws://localhost:8000")
        await manager.send_command("arm_1", {"action": "open_gripper"})
    """
    global _manager
    _manager = ROVManager(rov_uri)
    await _manager.start(gui_enabled=gui_enabled, **gui_config)
    return _manager


async def get_manager() -> Optional[ROVManager]:
    """Get the global manager instance."""
    return _manager

