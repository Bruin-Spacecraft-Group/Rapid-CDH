import board
import digitalio

import busio

import asyncio
import time

inter_subsystem_spi_bus = busio.SPI(
    board.SCK, MOSI=board.MOSI, MISO=board.MISO, slave_mode=True
)
while inter_subsystem_spi_bus.try_lock():
    time.sleep(0.1)
inter_subsystem_spi_bus.configure()  # baudrate, polarity, etc. available here as kw params


async def send_receive(transmit_buffer, receive_buffer):
    inter_subsystem_spi_bus.spi.write_readinto(transmit_buffer, receive_buffer)
