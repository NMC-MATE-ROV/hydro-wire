"""Advanced example showing integration with a main application.

Command Structure Note:
    Commands are structured with parameters grouped under "params" key.

    Your code:
        {"action": "pwm", "duty_cycle": 0.5, "enable": true}

    What gets sent:
        {"device": "led", "cmd": "pwm", "params": {"duty_cycle": 0.5, "enable": true}}
"""

import asyncio
import json
from typing import Dict, Any
from hydrowire import HydroWireManager as ROVManager


class MainApplication:
    """Example main application that integrates with rov-interface library."""

    def __init__(self, rov_uri: str = "ws://localhost:8000"):
        self.rov_manager = ROVManager(rov_uri)
        self.device_states: Dict[str, Any] = {}

    async def initialize(self):
        """Initialize the application."""
        print("Initializing main application...")
        await self.rov_manager.start()

        # Register custom handlers for specific command types
        self.rov_manager.register_command_handler("status", self.handle_status)
        self.rov_manager.register_command_handler("error", self.handle_error)

        print("Main application ready")

    async def handle_status(self, command: Dict[str, Any]):
        """Custom handler for status commands."""
        print(f"Status command received: {command}")
        return {"processed": True}

    async def handle_error(self, command: Dict[str, Any]):
        """Custom handler for error commands."""
        print(f"ERROR: {command}")
        return {"acked": True}

    async def control_arm(self, position: float, force: float = 50.0):
        """Control the ROV arm."""
        print(f"Controlling arm: position={position}, force={force}")
        response = await self.rov_manager.send_command(
            device_id="arm_1",
            command={
                "action": "move",
                "position": position,
                "force": force
            },
            expect_response=True
        )
        return response

    async def control_camera(self, action: str, **kwargs):
        """Control the main camera."""
        print(f"Controlling camera: action={action}")
        response = await self.rov_manager.send_command(
            device_id="camera_main",
            command={
                "action": action,
                **kwargs
            },
            expect_response=True
        )
        return response

    async def control_lights(self, brightness: int):
        """Control ROV lights."""
        print(f"Setting lights to {brightness}%")
        await self.rov_manager.send_command(
            device_id="lights",
            command={
                "action": "set_brightness",
                "level": brightness
            }
        )

    async def get_device_status(self, device_id: str):
        """Get status of a device."""
        response = await self.rov_manager.send_command(
            device_id=device_id,
            command={"action": "get_status"},
            expect_response=True
        )
        self.device_states[device_id] = response
        return response

    async def run_mission(self):
        """Example mission with multiple device interactions."""
        print("Starting mission...")

        try:
            # Step 1: Get status of all devices
            print("\n1. Checking device status...")
            for device in ["arm_1", "camera_main", "lights"]:
                status = await self.get_device_status(device)
                print(f"   {device}: {status}")

            # Step 2: Enable lights
            print("\n2. Enabling lights...")
            await self.control_lights(80)

            # Step 3: Position arm
            print("\n3. Moving arm to position...")
            await self.control_arm(position=90, force=75)

            # Step 4: Capture image
            print("\n4. Capturing image...")
            response = await self.control_camera(
                "capture",
                resolution="4k",
                format="jpg"
            )
            print(f"   Capture response: {response}")

            # Step 5: Return arm to neutral
            print("\n5. Returning arm to neutral...")
            await self.control_arm(position=0)

            print("\nMission completed successfully!")

        except Exception as e:
            print(f"Mission error: {e}")
            raise

    async def shutdown(self):
        """Shutdown the application."""
        print("Shutting down...")
        await self.rov_manager.close()


async def main():
    """Main entry point."""
    app = MainApplication()

    try:
        await app.initialize()

        # Run a mission
        await app.run_mission()

    except Exception as e:
        print(f"Application error: {e}")
    finally:
        await app.shutdown()


if __name__ == "__main__":
    asyncio.run(main())

