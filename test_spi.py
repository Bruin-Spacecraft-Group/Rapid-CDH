import board
import busio
import digitalio

cs = digitalio.DigitalInOut(board.Samuel)
cs.direction = digitalio.Direction.OUTPUT
cs.value = True

spi = busio.SPI(board.SCK, MISO=board.MISO)

while not spi.try_lock():
    pass

spi.configure(baudrate=5000000, phase=0, polarity=0)
cs.value = False
result = bytearray(4)
spi.readinto(result)
cs.value = True
result