# Installing and Using rov-interface

## Quick Start: Install from PyPI

The easiest way to use this library is to install it from PyPI:

```bash
pip install rov-interface
```

## Usage

Once installed, you can import and use the library from anywhere:

```python
import asyncio
from rov_lib import ROVManager

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
pip install rov-interface
```

### Install with Development Tools
```bash
pip install "rov-interface[dev]"
```

### From Source (for development)
```bash
git clone https://github.com/yourusername/rov-interface.git
cd rov-interface
pip install -e .
```

## Verifying Installation

Check if the package is installed:

```bash
pip show rov-interface
```

Quick test:

```bash
python -c "from rov_lib import ROVManager; print('✅ Ready to use!')"
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

