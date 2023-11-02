
import board
import busio
import digitalio
import time
cs = digitalio.DigitalInOut(board.D2)
cs.direction = digitalio.Direction.OUTPUT

led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT


spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)

while not spi.try_lock():
    pass
    
spi.configure(baudrate=200000, phase=0, polarity=0)
cs.value = False
prime_numbers = [161]
output = bytearray(prime_numbers)

spi.write(output)
    
cs.value = True