import board
import microcontroller
import digitalio
import busio
import spitarget

import asyncio
import time

inter_subsystem_spi_bus = spitarget.SPITarget(
    sck=board.D12,
    mosi=board.D13,
    miso=board.D11,
    ss=board.D10
)

async def send_receive(transmit_buffer, receive_buffer):
    inter_subsystem_spi_bus.load_packet(
        mosi_packet=receive_buffer,
        miso_packet=transmit_buffer
    )
    while not inter_subsystem_spi_bus.try_transfer():
        await asyncio.sleep(0)

sensorValue = 0x10203040
spiReadBytes = bytearray([0] * 4)
spiWriteBytes = bytearray([0] * 4)

async def spiWriteTask():
    global spiReadBytes, spiWriteBytes, sensorValue, inter_subsystem_spi_bus
    while True:
        # communicates commands with subsystem X
        spiWriteBytes[0] = (sensorValue & 0xFF000000) >> 24
        spiWriteBytes[1] = (sensorValue & 0xFF0000) >> 16
        spiWriteBytes[2] = (sensorValue & 0xFF00) >> 8
        spiWriteBytes[3] = (sensorValue & 0xFF) >> 0
        await send_receive(spiWriteBytes, spiReadBytes)

async def sensorReadTask():
    # regularly updates `sensorValue` based on the feedback from the sensor
    global sensorValue
    while True:
        sensorValue += 1
        await asyncio.sleep(0.2)

async def feedbackTask():
    # send debug data to the USB serial regularly
    global sensorValue, spiReadBytes, spiWriteBytes
    while True:
        print("TST wrote", list(bytes(spiWriteBytes)), "to SPI")  # fix with [:-1]
        print("TST read", list(bytes(spiReadBytes)), "from SPI")  # fix with [:-1]
        await asyncio.sleep(1)

async def gatheredTask():
    await asyncio.gather(feedbackTask(), spiWriteTask(), sensorReadTask())

asyncio.run(gatheredTask())
