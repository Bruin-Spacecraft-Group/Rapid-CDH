import board
import microcontroller
import digitalio
import busio


inter_subsystem_spi_bus = busio.SPI(
    board.SCK,
    MOSI=board.MOSI,
    MISO=microcontroller.pin.PA15,
    SS=board.MISO,
    slave_mode=True,
)
while inter_subsystem_spi_bus.try_lock():
    pass
inter_subsystem_spi_bus.configure()  # baudrate, polarity, etc. available here as kw params


def send_receive(transmit_buffer, receive_buffer):
    inter_subsystem_spi_bus.write_readinto(transmit_buffer, receive_buffer)


sensorValue = 0x8080
spiReadBytes = bytearray([0, 0, 0])
spiWriteBytes = bytearray([0, 0, 0])

while True:
    # communicates commands with subsystem X
    spiWriteBytes[0] = (sensorValue & 0xFF00) >> 8
    spiWriteBytes[1] = sensorValue & 0xFF
    send_receive(spiWriteBytes, spiReadBytes)
    sensorValue += 1
    if sensorValue % 1 == 0:
        print("TST wrote", list(bytes(spiWriteBytes))[:-1], "to SPI")
        print("TST read ", list(bytes(spiReadBytes))[:-1], "from SPI")
    busywait = 0
    while busywait < 100:
        busywait += 1
