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
        self._pins = dict()
        self._devices = dict()

    def _get_pin_reference(self, pin):
        if pin not in self._pins:
            self._pins[pin] = ManagedPin(pin)
        return self._pins[pin]

    def _create_general_device(self, pins, device_type, device_producer):
        m_pins = [self._get_pin_reference(pin) for pin in pins]
        device_key = tuple(m_pins + [device_type])
        if device_key not in self._devices:
            self._devices[device_key] = ManagedDevice(m_pins, device_producer)
        return self._devices[device_key]

    def create_digital_in_out(self, pin):
        return self._create_general_device(
            [pin],
            digitalio.DigitalInOut,
            (lambda: digitalio.DigitalInOut(pin)),
        )

    def create_spi(self, clock, MOSI, MISO):
        return self._create_general_device(
            [clock, MOSI, MISO],
            busio.SPI,
            (lambda: busio.SPI(clock, MOSI, MISO)),
        )

    def create_i2c(self, scl, sda, frequency=100000):
        return self._create_general_device(
            [scl, sda],
            busio.I2C,
            (lambda: busio.I2C(scl, sda, frequency=frequency)),
        )
