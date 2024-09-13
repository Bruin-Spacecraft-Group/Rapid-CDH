import board
import microcontroller
import digitalio
import busio

import asyncio
import time


from tasks.inter_subsystem_spi import (
    inter_subsystem_spi_task,
    inter_subsystem_spi_debug_task,
)


async def gathered_task():
    await asyncio.gather(inter_subsystem_spi_task(), inter_subsystem_spi_debug_task())


if __name__ == "__main__":
    asyncio.run(gathered_task())
