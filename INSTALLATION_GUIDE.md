# Installing and Using HydroWire

## Quick Start: Install from PyPI

The easiest way to use this library is to install it from PyPI:

```bash
pip install hydrowire
```

## Usage

Once installed, you can import and use the library from anywhere:

```python
import asyncio
from hydrowire import HydroWireManager as ROVManager

async def main():
    manager = ROVManager("ws://your-rov:8000")
    await manager.start()
    
    try:
        response = await manager.send_command(
            device_id="led",
            command={"action": "pwm", "duty_cycle": 0.5}
        )
        print(response)
    finally:
        await manager.close()

if __name__ == "__main__":
    asyncio.run(main())
```

## Installation Options

### Standard Installation
```bash
pip install hydrowire
```

### Install with Development Tools
```bash
pip install "hydrowire[dev]"
```

### From Source (for development)
```bash
git clone https://github.com/yourusername/hydrowire.git
cd hydrowire
pip install -e .
```

## Verifying Installation

Check if the package is installed:

```bash
pip show hydrowire
```

Quick test:

```bash
python -c "from hydrowire import HydroWireManager as ROVManager; print('✅ Ready to use!')"
```

## Requirements

- Python 3.9 or higher
- websockets >= 10.4

## Next Steps

See the main [README.md](README.md) for:
- Full API documentation
- Command structure details
- Complete examples
- Quick reference guide

