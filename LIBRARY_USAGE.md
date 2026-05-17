# Library Usage Guide for Main Applications

## Quick Summary

Your **HydroWire** library has been refactored to serve as a backend library for Python applications to interact with ROV systems. Here's what you now have:

## Core Features

✅ **Device-Targeted Commands** - Send commands to specific devices (arm, camera, lights, etc.)
✅ **Async/Await API** - Built on asyncio for efficient concurrent operations  
✅ **High-Level Manager** - Easy-to-use `ROVManager` class for your main app
✅ **Clean API** - Simple, intuitive function calls
✅ **GUI Ready** - Framework support for adding graphical interfaces later

## Using in Your Main Application

### Minimal Example

```python
import asyncio
from hydrowire import HydroWireManager as ROVManager

async def main():
    # Create and start manager
    manager = ROVManager("ws://your-rov:8000")
    await manager.start()
    
    try:
        # Send command to a device
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

### Command Format

Commands are automatically structured with parameters grouped under a `params` key:

```python
# Your code
await manager.send_command(
    device_id="led",
    command={"action": "pwm", "duty_cycle": 0.5, "enable": true}
)

# What gets sent over WebSocket
{
    "device": "led",
    "cmd": "pwm",
    "params": {
        "duty_cycle": 0.5,
        "enable": true
    }
}
```

The `action` key becomes `cmd`, `device_id` becomes `device`, and all other parameters are collected under `params`.

## API Reference

### Initialize
```python
manager = ROVManager(rov_uri, timeout=10.0)
```

### Start Communication
```python
await manager.start()
```

### Send Commands
```python
# Expecting a response
response = await manager.send_command(
    device_id="device_name",
    command={"action": "do_something"},
    expect_response=True
)

# Fire and forget
await manager.send_command(
    device_id="lights",
    command={"action": "on"}
)
```

### Cleanup
```python
await manager.close()
```

### Custom Integration
```python
# Register handlers for specific commands
manager.register_command_handler("status", my_handler)

# Attach GUI later
manager.attach_gui(my_gui_app)

# Run in blocking mode
await manager.run(gui_enabled=True, theme="dark")
```

## Directory Structure

```
hydrowire/
├── hydrowire/                    # Main library package
│   ├── __init__.py            # Exports: HydroWireManager, start, get_manager
│   ├── client.py              # Low-level WebSocket client
│   └── manager.py             # High-level HydroWireManager
├── examples/                   # Usage examples
│   ├── basic_usage.py         # Simple example
│   └── advanced_integration.py # Complex integration
├── tests/                      # Test suite (all passing ✓)
├── README.md                   # Full documentation
├── REFACTORING_NOTES.md        # What changed
└── requirements.txt            # Dependencies
```

## Common Device IDs

Your ROV might have these standard devices:
- `"arm_1"` - Manipulator arm
- `"camera_main"` - Primary camera
- `"lights"` - Lighting system
- `"thrusters"` - Propulsion
- `"sensors"` - Sensor package

(Adapt to your actual ROV configuration)

## Example Command Sequences

### Move and Capture
```python
# Move arm to position
await manager.send_command("arm_1", {"action": "move", "position": 45})

# Capture image
await manager.send_command(
    "camera_main",
    {"action": "capture", "format": "jpg"},
    expect_response=True
)

# Adjust lights
await manager.send_command("lights", {"action": "set_brightness", "level": 80})
```

### Mission-Style Operations
```python
async def perform_mission():
    # Get status
    status = await manager.send_command(
        "arm_1",
        {"action": "get_status"},
        expect_response=True
    )
    print(f"Arm status: {status}")
    
    # Execute sequence
    for position in [0, 45, 90, 45, 0]:
        await manager.send_command(
            "arm_1",
            {"action": "move", "position": position}
        )
        await asyncio.sleep(1)
```

## Testing

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=hydrowire
```

## Next Steps

1. **Connect your ROV backend** to the WebSocket address in `ROVManager`
2. **Define your device IDs** based on your ROV configuration
3. **Create command handlers** for your specific operations
4. **Build your main app** using `ROVManager` as the backend
5. **Later: Add GUI** using the `attach_gui()` method

## Important Notes

- ✨ The library is **async-first** - all operations use `async`/`await`
- 🔄 Always call `await manager.close()` for proper cleanup
- 📡 Commands are JSON-serialized automatically
- 🎯 Device ID routing happens on the backend
- 🛡️ Timeout protection on responses (default 10s)

## Getting Help

- See `REFACTORING_NOTES.md` for what changed during refactoring
- Check `examples/` directory for complete usage patterns
- Read `README.md` for comprehensive API documentation

---

**Your library is ready to use!** Start integrating it into your main application.

