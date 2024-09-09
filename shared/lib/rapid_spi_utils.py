import asyncio


async def async_transfer(spi_bus, device_cs, transmit_buffer, receive_buffer):
    device_cs.value = False
    spi_bus.async_transfer_start(transmit_buffer, receive_buffer)
    while not spi_bus.async_transfer_finished():
        await asyncio.sleep(0)
    spi_bus.async_transfer_end()
    device_cs.value = True
