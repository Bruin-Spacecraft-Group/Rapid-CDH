import board
import microcontroller
import digitalio
import busio

import asyncio
import time

from tasks.inter_subsystem_spi import (
    feedbackTask,
    spiWriteTask,
    sensorReadTask
)

async def gatheredTask():
    await asyncio.gather(feedbackTask(), spiWriteTask(), sensorReadTask())

asyncio.run(gatheredTask())