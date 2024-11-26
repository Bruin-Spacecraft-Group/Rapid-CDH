import digitalio
import busio


class ManagedPin:
    def __init__(self, pin):
        self.pin = pin
        self.is_claimed = False
        self.claimer = digitalio.DigitalInOut(self.pin)


class ManagedDevice:
    def __init__(self, managed_pins, device_producer):
        self._managed_pins = managed_pins
        self._device_producer = device_producer
        self._instance = None

    def __enter__(self):
        for m_pin in self._managed_pins:
            if m_pin.is_claimed:
                raise ValueError("Pin in use as " + str(type(m_pin.claimer)))
        for m_pin in self._managed_pins:
            m_pin.claimer.__exit__()
        self._instance = self._device_producer()
        for m_pin in self._managed_pins:
            m_pin.claimer = self._instance
            m_pin.is_claimed = True
        return self._instance

    def __exit__(self):
        self._instance.__exit__()
        for m_pin in self._managed_pins:
            m_pin.claimer.__exit__()
            m_pin.is_claimed = False
            m_pin.claimer = digitalio.DigitalInOut(m_pin.pin)


class PinManager:
    _instance = None

    def get_instance():
        if PinManager._instance is None:
            PinManager._instance = PinManager()
        return PinManager._instance

    def __init__(self):
        self._pins = []
        self._devices = []

    def _get_pin_reference(self, pin):
        if pin not in self._pins:
            self._pins[pin] = ManagedPin(pin)
        return self._pins[pin]

    # helper function to create a managed device when the constructor for the device
    # takes in only pin objects as parameters and has no positional arguments
    def _create_simple_device(self, pins, device_type):
        m_pins = [self._get_pin_reference(pin) for pin in pins]
        return ManagedDevice(m_pins, (lambda: device_type(*tuple(pins))))

    def create_digital_in_out(self, pin):
        return self._create_simple_device([pin], digitalio.DigitalInOut)

    def create_spi(self, clock, MOSI, MISO):
        return self._create_simple_device([clock, MOSI, MISO], busio.SPI)

    def create_i2c(self, scl, sda, frequency=100000):
        m_pins = [self._get_pin_reference(pin) for pin in [scl, sda]]
        return ManagedDevice(m_pins, (lambda: busio.I2C(scl, sda, frequency=frequency)))
