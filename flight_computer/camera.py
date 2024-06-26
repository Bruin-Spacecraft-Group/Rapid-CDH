from enum import Enum

import board
import busio
import digitalio
import asyncio

class Resolution(Enum):
    RES_320x240 = 1
    RES_640x480 = 2
    RES_1280x720 = 4
    RES_1600x1200 = 6
    RES_1920x1080 = 7
    RES_2592x1944 = 9
    RES_96x96 = 10
    RES_128x128 = 11
    RES_320x320 = 12

class Camera:
    def __init__(self, spi, cs):
        # Instantiates a camera using the provided SPI bus and chip select pin.
        # `spi` should be a `busio.SPI` object
        # `cs` should be a `Pin` object
        self.spi = spi
        self.cs = cs
        while not self.spi.try_lock(): # Not sure if this is needed
            pass
        self._regw_bufw = bytearray([0] * 2)
        self._regw_bufr = bytearray([0] * 2)
        self._regr_bufw = bytearray([0] * 3)
        self._regr_bufr = bytearray([0] * 3)
        self._last_byte = 0x00

    def _write_register(self, addr, value):
        # Writes a single sensor's internal register over SPI interface and sensor's register is accessed with 8 bit address and 8 bit data
        self._regw_bufw[0] = addr | 0x80
        self._regw_bufw[1] = value
        self.cs.value = False
        self.spi.write_readinto(self._regw_bufw, self._regw_bufr)
        self.cs.value = True

    def _read_register(self, addr):
        # Reads a single sensor's internal register over SPI interface and sensor's register is accessed with 8 bit address and 8 bit data
        self._regr_bufw[0] = addr & 0x7F
        self.cs.value = False
        self.spi.write_readinto(self._regr_bufw, self._regr_bufr)
        self.cs.value = True
        return self._regr_bufr[2]

    def _read_fifo_length(self):
        len1 = self._read_register(0x45)
        len2 = self._read_register(0x46)
        len3 = self._read_register(0x47)
        length = (len3 << 16) | (len2 << 8) | len1
        return length

    async def configure(self, resolution):
        # Sets up the camera for picture taking. This involves:
        # (1) configuring the chip select pin
        # (2) sending some SPI commands to the camera.
        # This method expects that the lock on `self.spi` is already held and that the
        # SPI bus itself is already properly configured, since this bus may be shared.
        self.cs.direction = digitalio.Direction.OUTPUT
        self.cs.value = True
        self._write_register(0x07, (1 << 6))
        self._write_register(0x20, 0x01)
        self._write_register(0x21, resolution)

    async def generate_image(self):
        # Returns a generator that produces each byte of a captured image

        # start capture and wait for it to finish
        self._write_register(0x04, (1 << 0))
        self._write_register(0x04, (1 << 1))
        while self._read_register(0x44) & (1 << 2):
            await asyncio.sleep(0)  

        # read the buffer over SPI and return it through the generator
        length = self._read_fifo_length()
        processing_state = 0
        while length > 0:
            this_byte = self._read_register(0x3D)
            await asyncio.sleep(0)
            if (self._last_byte == 0xFF) and (this_byte == 0xD8):
                yield 0xFF
                processing_state = 1
            if processing_state == 1:
                yield this_byte
            if (self._last_byte == 0xFF) and (this_byte == 0xD9):
                processing_state == 2
            self._last_byte = this_byte
            length -= 1

    async def generate_image_burst_read(self):
        # start capture and wait for it to finish
        self._write_register(0x04, (1 << 0))
        self._write_register(0x04, (1 << 1))
        while self._read_register(0x44) & (1 << 2):
            await asyncio.sleep(0)  

        # burst read the buffer over SPI
        burst_size = 128
        readbuf = bytearray(burst_size)
        count = 0
        length = self._read_fifo_length()
        self.cs.value = False
        regbuff = bytearray(1)
        regbuff[0] = 0x3C
        self.spi.write(regbuff, start=0, end=1)

        while count+burst_size <= length:
            self.spi.readinto(readbuf, start=0, end=burst_size)
            yield readbuf
            await asyncio.sleep(0)
            count += burst_size
        
        count = length - count # get the leftovers
        readbuf = bytearray(burst_size) # reset readbuf
        self.spi.readinto(readbuf, start=0, end=count)
        yield readbuf
        self.cs.value = True

        self._write_register(0x04, (1 << 0))

