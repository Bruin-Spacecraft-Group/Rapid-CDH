import board
import microcontroller
import digitalio
import busio

import asyncio
import time

inter_subsystem_spi_bus = busio.SPI(
    clock=board.D12,
    MOSI=board.D13,
    MISO=board.D11,
    SS=board.D10,
    slave_mode=True,
)
while inter_subsystem_spi_bus.try_lock():
    pass
inter_subsystem_spi_bus.configure()  # baudrate, polarity, etc. available here as kw params


async def send_receive(transmit_buffer, receive_buffer):
    inter_subsystem_spi_bus.async_transfer_start(transmit_buffer, receive_buffer)
    while not inter_subsystem_spi_bus.async_transfer_finished():
        await asyncio.sleep(0)
    inter_subsystem_spi_bus.async_transfer_end()


sensorValue = 0x10203040
spiReadBytes = bytearray([0] * 4)
spiWriteBytes = bytearray([0] * 4)


async def spiWriteTask():
    global spiReadBytes, spiWriteBytes, sensorValue, inter_subsystem_spi_bus
    while True:
        # communicates data back to CDH
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
    await asyncio.gather(spiWriteTask(), sensorReadTask(), feedbackTask())


asyncio.run(gatheredTask())
