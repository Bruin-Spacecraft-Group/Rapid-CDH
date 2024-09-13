import busio
import spitarget

import asyncio


class spi_bus(busio.SPI):
    def __init__(self, clock, MOSI=None, MISO=None, half_duplex=False):
        self.init_clock = clock
        self.init_MOSI = MOSI
        self.init_MISO = MISO
        busio.SPI.__init__(self, clock, MOSI, MISO, half_duplex)

    def get_clock_pin(self):
        return self.init_clock

    def get_MOSI_pin(self):
        return self.init_MOSI

    def get_MISO_pin(self):
        return self.init_MISO


class spi_device:
    def __init__(self, spi, chip_select):
        self.init_spi = spi
        self.init_chip_select = chip_select
        chip_select.switch_to_output(value=True)

    async def async_transfer(self, transmit_buffer, receive_buffer):
        while not self.init_spi.try_lock():
            await asyncio.sleep(0)
        self.init_chip_select.value = False
        self.init_spi.async_transfer_start(transmit_buffer, receive_buffer)
        while not self.init_spi.async_transfer_finished():
            await asyncio.sleep(0)
        self.init_spi.async_transfer_end()
        self.init_chip_select.value = True
        self.init_spi.unlock()

    def get_spi(self):
        return self.init_spi

    def get_clock_pin(self):
        return self.init_spi.get_clock_pin()

    def get_MOSI_pin(self):
        return self.init_spi.get_MOSI_pin()

    def get_MISO_pin(self):
        return self.init_spi.get_MISO_pin()

    def get_chip_select_pin(self):
        return self.init_chip_select


# class spi_target(spitarget.SPITarget):
#     TODO: enable and test this class once the firmware refactor is stable
#     def __init__(self, clock, MOSI, MISO, CS):
#         self.init_clock = clock
#         self.init_MOSI = MOSI
#         self.init_MISO = MISO
#         self.init_CS = CS
#         spitarget.SPITarget.__init__(self, clock, MOSI, MISO, CS)

#     def get_clock_pin(self):
#         return self.init_clock

#     def get_MOSI_pin(self):
#         return self.init_MOSI

#     def get_MISO_pin(self):
#         return self.init_MISO

#     def get_chip_select_pin(self):
#         return self.init_CS
