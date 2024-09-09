# import busio

import asyncio

ADS1118_VCC = 3.3


class ADS1118:
    def __init__(self, spi_bus, chip_select):
        self.readings = [None, None, None, None]

    # async def get??? TODO finish the driver implementation

    def get_channel_1_voltage(self):
        return
