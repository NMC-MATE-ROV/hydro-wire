import asyncio
import json

import pytest
import websockets

from hydrowire.client import WebSocketCommandClient
from hydrowire.manager import HydroWireManager as ROVManager


@pytest.mark.asyncio
async def test_send_command_with_device_id():
    """Test sending a command to a specific device with params structure."""
    async def handler(ws):
        msg = await ws.recv()
        data = json.loads(msg)
        # Validate the params structure
        assert "device" in data
        assert data["device"] == "led"
        assert "cmd" in data
        assert data["cmd"] == "pwm"
        assert "params" in data
        assert data["params"]["duty_cycle"] == 0.5
        assert data["params"]["enable"] == True
        await ws.send(json.dumps({"status": "success"}))

    server = await websockets.serve(handler, "localhost", 8765)
    try:
        async with WebSocketCommandClient("ws://localhost:8765") as client:
            resp = await client.send_command(
                device_id="led",
                command={"action": "pwm", "duty_cycle": 0.5, "enable": True},
                expect_response=True
            )
            assert resp == {"status": "success"}
    finally:
        server.close()
        await server.wait_closed()


@pytest.mark.asyncio
async def test_rov_manager_send_command():
    """Test ROVManager sending commands with params structure."""
    async def handler(ws):
        msg = await ws.recv()
        data = json.loads(msg)
        assert data["device"] == "camera_main"
        assert data["cmd"] == "capture"
        assert "params" in data
        assert data["params"]["resolution"] == "4k"
        await ws.send(json.dumps({"status": "captured"}))

    server = await websockets.serve(handler, "localhost", 8766)
    try:
        manager = ROVManager("ws://localhost:8766")
        await manager.initialize()
        resp = await manager.send_command(
            device_id="camera_main",
            command={"action": "capture", "resolution": "4k"},
            expect_response=True
        )
        assert resp == {"status": "captured"}
        await manager.close()
    finally:
        server.close()
        await server.wait_closed()
