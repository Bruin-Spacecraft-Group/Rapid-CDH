import board
import digitalio

import busio
from adafruit_bus_device.spi_device import SPIDevice

inter_subsystem_spi_bus = busio.SPI(
    board.SCK, MOSI=board.MOSI, MISO=board.MISO, slave_mode=False
)

test_board_cs = digitalio.DigitalInOut(board.D2)
test_board_cs.direction = digitalio.Direction.OUTPUT
test_board = SPIDevice(
    inter_subsystem_spi_bus, test_board_cs
)  # baudrate, polarity, etc. available here as kw params


def send_receive(transmit_buffer, receive_buffer):
    with test_board as spi:
        spi.write_readinto(transmit_buffer, receive_buffer)


sensorValue = 0x0000
spiReadBytes = bytearray([0, 0, 0])
spiWriteBytes = bytearray([0, 0, 0])

while True:
    # communicates commands with subsystem X
    spiWriteBytes[0] = (sensorValue & 0xFF00) >> 8
    spiWriteBytes[1] = sensorValue & 0xFF
    send_receive(spiWriteBytes, spiReadBytes)
    sensorValue += 1
    if sensorValue % 1 == 0:
        print("CDH wrote", list(bytes(spiWriteBytes))[:-1], "to SPI")
        print("CDH read ", list(bytes(spiReadBytes))[1:], "from SPI")
    busywait = 0
    while busywait < 100000:
        busywait += 1
