import sys
import os
import pytest
from unittest import mock

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'shared', 'lib')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'shared', 'drivers')))

import ads1118
import spi
import board
import busio


def test_ads1118_init():
    ads_spi_device = spi.spi_device(spi.spi_bus(clock=board.D12, MOSI=board.D13, MISO=board.D11), board.D10)
    ads = ads1118.ADS1118(ads_spi_device) # ideally wrap this in a pytest fixture but i haven't figured out them yet
    assert ads.spi_device is not None
    assert ads.data_ready is not None