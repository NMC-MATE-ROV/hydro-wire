# rov-interface - Quick Reference Card

## 🚀 Quick Start

```python
import asyncio
from rov_lib import ROVManager

async def main():
    manager = ROVManager("ws://localhost:8000")
    await manager.start()
    
    # Send command
    response = await manager.send_command(
        device_id="arm_1",
        command={"action": "move", "position": 45},
        expect_response=True
    )
    
    await manager.close()

asyncio.run(main())
```

## 📦 Imports

```python
# High-level (recommended)
from rov_lib import ROVManager, start, get_manager

# Low-level (if needed)
from rov_lib import WebSocketCommandClient
```

## 🎯 Send Command Patterns

### With Response
```python
response = await manager.send_command(
    device_id="camera_1",
    command={"action": "capture"},
    expect_response=True
)
# response is a dict with server's reply
```

### Fire and Forget
```python
await manager.send_command(
    device_id="lights",
    command={"action": "on"}
)
# No response wait
```

### Simple Action
```python
await manager.send_command(
    "device_id",
    {"action": "something"}
)
```

## 🔧 Manager Methods

| Method | Purpose |
|--------|---------|
| `__init__(uri, timeout=10)` | Create manager |
| `await start()` | Initialize connection |
| `await send_command(id, cmd, expect_response=False)` | Send command to device |
| `await close()` | Close connection |
| `await run()` | Blocking run mode |
| `attach_gui(app)` | Attach GUI (future) |
| `register_command_handler(type, handler)` | Register handler |

## 📡 Command Structure

**What you send:**
```python
{"action": "pwm", "duty_cycle": 0.5, "enable": true}
```

**What goes over WebSocket (structured):**
```python
{
    "device": "led",
    "cmd": "pwm",
    "params": {
        "duty_cycle": 0.5,
        "enable": true
    }
}
```

The library automatically groups parameters under the `params` key.

## 🏗️ Project Structure

```
rov_lib/
├── __init__.py          # Package exports
├── client.py            # WebSocket client (low-level)
└── manager.py           # ROVManager (high-level)

examples/
├── basic_usage.py       # Simple example
└── advanced_integration.py  # Complex example

tests/
└── test_client.py       # Test suite (all passing ✓)
```

## 📚 Documentation Files

| File | Purpose |
|------|---------|
| `README.md` | Full documentation & API reference |
| `LIBRARY_USAGE.md` | Guide for using in main apps |
| `REFACTORING_NOTES.md` | What changed during refactoring |
| `QUICK_REFERENCE.md` | This cheat sheet |

## 🧪 Testing

```bash
# Run tests
pytest tests/ -v

# Test specific test
pytest tests/test_client.py::test_send_command_with_device_id -v
```

## 📋 Common Tasks

### Create Manager
```python
manager = ROVManager("ws://localhost:8000")
```

### Start/Stop
```python
await manager.start()      # Connect & initialize
await manager.close()      # Disconnect
```

### Send to Device
```python
await manager.send_command("device_id", {"action": "do_thing"})
```

### Control Arm
```python
await manager.send_command("arm_1", {
    "action": "move",
    "position": 45,
    "speed": 10
})
```

### Capture Image
```python
img = await manager.send_command("camera_main", {
    "action": "capture",
    "format": "jpg",
    "resolution": "4k"
}, expect_response=True)
```

### Set Lights
```python
await manager.send_command("lights", {
    "action": "set_brightness",
    "level": 80
})
```

### Get Status
```python
status = await manager.send_command(
    "device_id",
    {"action": "get_status"},
    expect_response=True
)
```

## 🔌 Installation

```bash
pip install -r requirements.txt
```

## ✨ Features at a Glance

- ✅ Device-targeted commands
- ✅ Async/await API
- ✅ WebSocket communication
- ✅ Response handling
- ✅ Error handling with timeouts
- ✅ GUI framework ready
- ✅ Type hints
- ✅ Full test coverage

## 📞 Support

- See `README.md` for detailed API docs
- Check `examples/` for usage patterns
- Read `REFACTORING_NOTES.md` for architecture info

---

**Ready to use!** Import `ROVManager` and start building your app.

