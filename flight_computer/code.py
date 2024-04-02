import asyncio
import time

sensorValue = 0
spiReadBytes = bytearray([0, 0])
spiWriteBytes = bytearray([0, 0])


async def spiWriteTask():
    global spiReadBytes, spiWriteBytes
    from inter_subsystem_spi import send_receive

    while True:
        # communicates commands with subsystem X
        spiWriteBytes[0] = (sensorValue & 0xFF00) >> 8
        spiWriteBytes[1] = sensorValue & 0xFF
        await send_receive(spiWriteBytes, spiReadBytes)
        await asyncio.sleep(0.9)


async def sensorReadTask():
    # regularly updates `sensorValue` based on the feedback from the sensor
    global sensorValue
    while True:
        sensorValue += 1
        await asyncio.sleep(2.3)


async def feedbackTask():
    # send debug data to the USB serial regularly
    global sensorValue, spiReadBytes, spiWriteBytes
    while True:
        print("Wrote", list(bytes(spiWriteBytes)), "to SPI")
        print("Read", list(bytes(spiReadBytes)), "from SPI")
        await asyncio.sleep(1)


async def idleTask():
    while True:
        # Forces CircuitPython to call `RUN_BACKGROUND_TASKS` at 10Hz to maintain USB connection
        await asyncio.sleep(0.02)
        await time.sleep(0.02)


async def gatheredTask():
    await asyncio.gather(spiWriteTask(), sensorReadTask(), feedbackTask(), idleTask())


asyncio.run(gatheredTask())
