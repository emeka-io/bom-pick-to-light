import time
from typing import Optional


class SerialDriver:
    """Manages host-to-MCU packet formatting, framing, and communication."""

    def __init__(self, port: str = "COM3", baud_rate: int = 115200, timeout: float = 1.0):
        self.port = port
        self.baud_rate = baud_rate
        self.timeout = timeout
        self.is_connected = False

    @staticmethod
    def format_packet(command: str, bin_id: str, color_hex: str, qty: int) -> str:
        """Formats a command frame: CMD:PICK|BIN_ID|COLOR|QTY\n"""
        payload = f"{command}:{bin_id}|{color_hex}|{qty}"
        return f"{payload}\n"

    def connect(self) -> bool:
        """Simulates connection establishment to the target hardware port."""
        self.is_connected = True
        return True

    def send_pick_command(self, bin_id: str, color_hex: str = "00FF00", qty: int = 1) -> str:
        """Dispatches an active pick instruction frame to the MCU."""
        if not self.is_connected:
            raise ConnectionError("Serial port is not connected. Call connect() first.")

        packet = self.format_packet("SET_LED", bin_id, color_hex, qty)
        return packet.strip()

    def disconnect(self) -> None:
        """Closes the active serial connection."""
        self.is_connected = False
