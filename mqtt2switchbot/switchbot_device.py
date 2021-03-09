import logging
import asyncio
from bleak import BleakClient
from bleak.exc import BleakError
from typing import List

_LOGGER = logging.getLogger(__name__)

UUID = "cba20002-224d-11e6-9fb8-0002a5d5c51b"


class ExecutionError(Exception):
    pass


class SwitchbotDevice:
    def __init__(self, mac_address):
        self.mac_address = mac_address

    def execute(self, payload, command):
        inner_loop = asyncio.new_event_loop()
        inner_loop.run_until_complete(self._execute(command))
        inner_loop.close()

    async def _execute(self, command):
        bleak_client = None
        try:
            bleak_client = await self._connect()
            if command:
                await bleak_client.write_gatt_char(UUID, bytearray(command))

                res = "await bleak_client.read_gatt_char(UUID)"
                self.set_device_status(res)
            else:
                _LOGGER.error("Noting to execute")
        except BleakError as e:
            _LOGGER.error(f"Failed to execute. Error: {e}")
            raise ExecutionError
        finally:
            await bleak_client.disconnect()

    async def _connect(self):
        try:
            bleak_client = BleakClient(self.mac_address)
            await bleak_client.connect()
            return bleak_client
        except BleakError as e:
            _LOGGER.error(f"Unable to connect. Error: {e}")
            raise ConnectionError


class Curtain(SwitchbotDevice):
    FAST = 0xff
    SILENT = 0x01

    def __init__(self, mac_address, silent_mode: bool = False):
        super().__init__(mac_address)
        self.mode = self.SILENT if silent_mode else self.FAST
        self.position: int

    def execute(self, payload, command=None):
        command = self._command(payload)
        super().execute(payload, command)

    def _command(self, payload: bytes) -> List:
        try:
            if payload == b"OPEN":
                self.position = 0
                return [0x57, 0x0f, 0x45, 0x01, 0x05, self.mode, 0x00]
            elif payload == b"CLOSE":
                self.position = 100
                return [0x57, 0x0f, 0x45, 0x01, 0x05, self.mode, 0x64]
            elif payload == b"STOP":
                return [0x57, 0x0f, 0x45, 0x01, 0x00, 0xFF]
            else:
                position = int(payload)
                if 0 <= position <= 100:
                    self.position = position
                    return [0x57, 0x0f, 0x45, 0x01, 0x05, self.mode, position]

                return []
        except ValueError:
            _LOGGER.error("Unknown command. Valid values are OPEN, CLOSE, STOP or a position (0-100)")
            raise ValueError

    def get_state(self):
        return self.position
