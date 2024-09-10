import unittest

import ads1118


class TestStringMethods(unittest.TestCase):

    def test_parameter_validation(self):
        # Test with good parameters

        failure = None
        try:
            ads1118.ADS1118._check_sampling_params(
                ads1118.ADS1118_MUX_SELECT.CH0_CH1_DIFF,
                ads1118.ADS1118_FSR.FSR_6144V,
                ads1118.ADS1118_SAMPLE_RATE.RATE_8,
            )
        except AssertionError as e:
            failure = e
        self.assertIsNone(failure)

        failure = None
        try:
            ads1118.ADS1118._check_sampling_params(
                ads1118.ADS1118_MUX_SELECT.CH3_SINGLE_END,
                ads1118.ADS1118_FSR.FSR_0256V,
                ads1118.ADS1118_SAMPLE_RATE.RATE_860,
            )
        except AssertionError as e:
            failure = e
        self.assertIsNone(failure)

        failure = None
        try:
            ads1118.ADS1118._check_sampling_params(
                ads1118.ADS1118_MUX_SELECT.CH0_SINGLE_END,
                ads1118.ADS1118_FSR.FSR_4096V,
                ads1118.ADS1118_SAMPLE_RATE.RATE_128,
            )
        except AssertionError as e:
            failure = e
        self.assertIsNone(failure)

        failure = None
        try:
            ads1118.ADS1118._check_sampling_params(
                ads1118.ADS1118_MUX_SELECT.TEMPERATURE,
                ads1118.ADS1118_FSR.FSR_2048V,
                ads1118.ADS1118_SAMPLE_RATE.RATE_475,
            )
        except AssertionError as e:
            failure = e
        self.assertIsNone(failure)

        # Test with bad parameters

        self.assertRaises(
            AssertionError, ads1118.ADS1118._check_sampling_params, -1, 0, 0
        )
        self.assertRaises(
            AssertionError, ads1118.ADS1118._check_sampling_params, 8, 0, 0
        )
        self.assertRaises(
            AssertionError, ads1118.ADS1118._check_sampling_params, 254, 0, 0
        )
        self.assertRaises(
            AssertionError, ads1118.ADS1118._check_sampling_params, 256, 0, 0
        )
        self.assertRaises(
            AssertionError, ads1118.ADS1118._check_sampling_params, 4.5, 0, 0
        )

        self.assertRaises(
            AssertionError, ads1118.ADS1118._check_sampling_params, 0, -1, 0
        )
        self.assertRaises(
            AssertionError, ads1118.ADS1118._check_sampling_params, 0, 8, 0
        )
        self.assertRaises(
            AssertionError, ads1118.ADS1118._check_sampling_params, 0, 4.5, 0
        )

        self.assertRaises(
            AssertionError, ads1118.ADS1118._check_sampling_params, 0, 0, -1
        )
        self.assertRaises(
            AssertionError, ads1118.ADS1118._check_sampling_params, 0, 0, 8
        )
        self.assertRaises(
            AssertionError, ads1118.ADS1118._check_sampling_params, 0, 0, 4.5
        )

    def test_config_register_format(self):
        self.assertEqual(
            ads1118.ADS1118._build_config_register_bytearray(
                ads1118.ADS1118_MUX_SELECT.CH0_SINGLE_END,
                ads1118.ADS1118_FSR.FSR_4096V,
                ads1118.ADS1118_SAMPLE_RATE.RATE_128,
            ),
            b"\xC3\x8A",
        )
        self.assertEqual(
            ads1118.ADS1118._build_config_register_bytearray(
                ads1118.ADS1118_MUX_SELECT.CH2_CH3_DIFF,
                ads1118.ADS1118_FSR.FSR_2048V,
                ads1118.ADS1118_SAMPLE_RATE.RATE_860,
            ),
            b"\xB5\xEA",
        )
        self.assertEqual(
            ads1118.ADS1118._build_config_register_bytearray(
                ads1118.ADS1118_MUX_SELECT.CH0_CH1_DIFF,
                ads1118.ADS1118_FSR.FSR_6144V,
                ads1118.ADS1118_SAMPLE_RATE.RATE_8,
            ),
            b"\x81\x0A",
        )
        self.assertEqual(
            ads1118.ADS1118._build_config_register_bytearray(
                ads1118.ADS1118_MUX_SELECT.TEMPERATURE,
                ads1118.ADS1118_FSR.FSR_0256V,
                ads1118.ADS1118_SAMPLE_RATE.RATE_64,
            ),
            b"\xFB\x7A",
        )

    def test_temperature_conversion(self):
        self.assertAlmostEqual(
            ads1118.ADS1118._temperature_from_bytes(
                bytes([0b_01_0000_00, 0b_00_0000_00])
            ),
            128,
        )
        self.assertAlmostEqual(
            ads1118.ADS1118._temperature_from_bytes(
                bytes([0b_00_1111_11, 0b_11_1111_00])
            ),
            127.96875,
        )
        self.assertAlmostEqual(
            ads1118.ADS1118._temperature_from_bytes(
                bytes([0b_00_1100_10, 0b_00_0000_00])
            ),
            100,
        )
        self.assertAlmostEqual(
            ads1118.ADS1118._temperature_from_bytes(
                bytes([0b_00_1001_01, 0b_10_0000_00])
            ),
            75,
        )
        self.assertAlmostEqual(
            ads1118.ADS1118._temperature_from_bytes(
                bytes([0b_00_0110_01, 0b_00_0000_00])
            ),
            50,
        )
        self.assertAlmostEqual(
            ads1118.ADS1118._temperature_from_bytes(
                bytes([0b_00_0011_00, 0b_10_0000_00])
            ),
            25,
        )
        self.assertAlmostEqual(
            ads1118.ADS1118._temperature_from_bytes(
                bytes([0b_00_0000_00, 0b_00_1000_00])
            ),
            0.25,
        )
        self.assertAlmostEqual(
            ads1118.ADS1118._temperature_from_bytes(
                bytes([0b_00_0000_00, 0b_00_0001_00])
            ),
            0.03125,
        )
        self.assertAlmostEqual(
            ads1118.ADS1118._temperature_from_bytes(
                bytes([0b_00_0000_00, 0b_00_0000_00])
            ),
            0,
        )
        self.assertAlmostEqual(
            ads1118.ADS1118._temperature_from_bytes(
                bytes([0b_00_0000_00, 0b_00_0000_10])
            ),
            0,
        )
        self.assertAlmostEqual(
            ads1118.ADS1118._temperature_from_bytes(
                bytes([0b_00_0000_00, 0b_00_0000_01])
            ),
            0,
        )
        self.assertAlmostEqual(
            ads1118.ADS1118._temperature_from_bytes(
                bytes([0b_11_1111_11, 0b_11_1000_00])
            ),
            -0.25,
        )
        self.assertAlmostEqual(
            ads1118.ADS1118._temperature_from_bytes(
                bytes([0b_11_1100_11, 0b_10_0000_00])
            ),
            -25,
        )
        self.assertAlmostEqual(
            ads1118.ADS1118._temperature_from_bytes(
                bytes([0b_11_1011_00, 0b_00_0000_00])
            ),
            -40,
        )

    def test_voltage_conversion(self):
        self.assertAlmostEqual(
            ads1118.ADS1118._voltage_from_bytes(
                b"\x7F\xFF", ads1118.ADS1118_FSR.FSR_4096V
            ),
            4.096 * (2**15 - 1) / (2**15),
        )
        self.assertAlmostEqual(
            ads1118.ADS1118._voltage_from_bytes(
                b"\x00\x01", ads1118.ADS1118_FSR.FSR_4096V
            ),
            4.096 / (2**15),
        )
        self.assertAlmostEqual(
            ads1118.ADS1118._voltage_from_bytes(
                b"\x00\x00", ads1118.ADS1118_FSR.FSR_4096V
            ),
            0,
        )
        self.assertAlmostEqual(
            ads1118.ADS1118._voltage_from_bytes(
                b"\xFF\xFF", ads1118.ADS1118_FSR.FSR_4096V
            ),
            -4.096 / (2**15),
        )
        self.assertAlmostEqual(
            ads1118.ADS1118._voltage_from_bytes(
                b"\x80\x00", ads1118.ADS1118_FSR.FSR_4096V
            ),
            -4.096,
        )
        self.assertAlmostEqual(
            ads1118.ADS1118._voltage_from_bytes(
                b"\x7F\xFF", ads1118.ADS1118_FSR.FSR_0256V
            ),
            0.256 * (2**15 - 1) / (2**15),
        )
        self.assertAlmostEqual(
            ads1118.ADS1118._voltage_from_bytes(
                b"\x00\x01", ads1118.ADS1118_FSR.FSR_0256V
            ),
            0.256 / (2**15),
        )
        self.assertAlmostEqual(
            ads1118.ADS1118._voltage_from_bytes(
                b"\x00\x00", ads1118.ADS1118_FSR.FSR_0256V
            ),
            0,
        )
        self.assertAlmostEqual(
            ads1118.ADS1118._voltage_from_bytes(
                b"\xFF\xFF", ads1118.ADS1118_FSR.FSR_0256V
            ),
            -0.256 / (2**15),
        )
        self.assertAlmostEqual(
            ads1118.ADS1118._voltage_from_bytes(
                b"\x80\x00", ads1118.ADS1118_FSR.FSR_0256V
            ),
            -0.256,
        )


if __name__ == "__main__":
    unittest.main()
