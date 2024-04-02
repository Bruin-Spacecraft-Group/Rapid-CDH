import board
import digitalio

import busio
from adafruit_bus_device.spi_device import SPIDevice

import asyncio

inter_subsystem_spi_bus = busio.SPI(
    board.SCK, MOSI=board.MOSI, MISO=board.MISO, slave_mode=False
)

test_board_cs = digitalio.DigitalInOut(board.D2)
test_board_cs.direction = digitalio.Direction.OUTPUT
test_board = SPIDevice(
    inter_subsystem_spi_bus, test_board_cs
)  # baudrate, polarity, etc. available here as kw params


async def send_receive(transmit_buffer, receive_buffer):
    with test_board as spi:
        spi.write_readinto(transmit_buffer, receive_buffer)
