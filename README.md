# rov-interface

A Python library for applications to interact with ROV (Remotely Operated Vehicle) systems over WebSocket.

## Installation

### From PyPI (Recommended)

```bash
pip install rov-interface
```

### From Source (Development)

```bash
git clone https://github.com/yourusername/rov-interface.git
cd rov-interface
pip install -e .
```

## Features

- 🔌 **WebSocket Communication**: Send JSON commands to ROV devices
- 🎯 **Device Targeting**: Route commands to specific devices using device IDs
- ⚙️ **Async-First Design**: Built on asyncio for efficient concurrent operations
- 🎨 **GUI Ready**: Framework for integrating graphical interfaces
- 📦 **Library-First**: Designed to be embedded in main applications

## Installation

```bash
pip install -r requirements.txt
```

For development:

```bash
pip install -r dev-requirements.txt
```

## Quick Start

### Basic Usage

```python
import asyncio
from rov_lib import ROVManager

async def main():
    # Initialize manager
    manager = ROVManager("ws://localhost:8000")
    
    # Start communication
    await manager.start()
    
    try:
        # Send a command to a device
        response = await manager.send_command(
            device_id="arm_1",
            command={"action": "move", "position": 45},
            expect_response=True
        )
        print(response)
    finally:
        await manager.close()

asyncio.run(main())
```

### Using the Global Start Function

```python
import asyncio
from rov_lib import start

async def main():
    # Quick start with convenience function
    manager = await start("ws://localhost:8000")
    
    try:
        await manager.send_command(
            device_id="camera_main",
            command={"action": "capture"}
        )
    finally:
        await manager.close()

asyncio.run(main())
```

## API Reference

### ROVManager

The main class for interacting with ROV systems.

#### Initialization

```python
manager = ROVManager(rov_uri, timeout=10.0)
```

- `rov_uri` (str): WebSocket URI for ROV (e.g., `ws://localhost:8000`)
- `timeout` (float): Command timeout in seconds (default: 10.0)

#### Methods

**`async initialize()`**: Initialize connection to ROV

**`async start(gui_enabled=False, **gui_config)`**: Start the ROV manager and optionally launch GUI

**`async send_command(device_id, command, expect_response=False)`**: Send a command to a device

- `device_id` (str): Target device identifier (e.g., "arm_1", "camera_main")
- `command` (dict): Command object with action and parameters
- `expect_response` (bool): Wait for response if True
- Returns: Response dict if `expect_response=True`, otherwise None

**`async close()`**: Close ROV connection

**`async run(gui_enabled=False, **gui_config)`**: Run manager in blocking mode

**`attach_gui(gui_app)`**: Attach GUI application instance

**`register_command_handler(command_type, handler)`**: Register custom command handler

### Global Functions

**`async start(rov_uri, gui_enabled=False, **gui_config)`**: Convenience function to create and start a manager

**`async get_manager()`**: Get the global manager instance

## Command Structure

Commands are sent with a structured format where parameters are grouped under a `params` key:

**Your code:**
```python
await manager.send_command(
    device_id="led",
    command={"action": "pwm", "duty_cycle": 0.5, "enable": true}
)
```

**What gets sent over WebSocket:**
```json
{
  "device": "led",
  "cmd": "pwm",
  "params": {
    "duty_cycle": 0.5,
    "enable": true
  }
}
```

This structured format makes it easy for the ROV backend to:
- Route commands to the correct device
- Access the command type directly
- Parse all parameters from a single `params` object

## Running Tests

```bash
pytest tests/ -v
```

## Examples

See the `examples/` directory for more detailed usage patterns.

## Architecture

- **`rov_lib/client.py`**: Low-level WebSocket client
- **`rov_lib/manager.py`**: High-level manager with device routing
- **`rov_lib/__init__.py`**: Package exports

## Future Enhancements

- GUI framework integration
- Device discovery and management
- Command queuing and priority
- Connection recovery and reconnection
- Telemetry and logging

## License

(To be determined)

