#Task for sending data to the ground station
#We're passed a state vector

#from Tasks.template_task import task

from task import Task
from enum import Enum
from satio import *

class CommsModes(Enum):
    SCANNING = 0
    TRANSMITTING = 1

class Data():
    timestamp = 0
    def encode():
        return "not implemented!"

# EPS data
class EpsData(Data):
    eps_volt_1 = 0      # 4 bytes float
    eps_volt_2 = 0      # 4 bytes float
    # ...

    def encode(self):
        encoded_data = []
        encoded_data.append(self.timestamp.to_bytes(4, 'little')) # 4 bytes float

        encoded_data.append(self.eps_volt_1.to_bytes(4, 'little')) # 4 bytes float
        encoded_data.append(self.eps_volt_2.to_bytes(4, 'little')) # 4 bytes float
        return encoded_data

# Prop data
class PropData(Data):
    prop_press_1 = 0    # 4 bytes float
    prop_press_2 = 0    # 4 bytes float
    prop_temp_1 = 0     # 4 bytes float
    prop_temp_2 = 0     # 4 bytes float
    prop_power_i_1 = 0  # 4 bytes float
    prop_power_i_2 = 0  # 4 bytes float
    prop_power_v_1 = 0  # 4 bytes float
    prop_power_v_2 = 0  # 4 bytes float
    # ...

    def encode(self):
        encoded_data = []
        encoded_data.append(self.timestamp.to_bytes(4, 'little')) # 4 bytes float

        encoded_data.append(self.prop_press_1.to_bytes(4, 'little')) # 4 bytes float
        encoded_data.append(self.prop_press_2.to_bytes(4, 'little')) # 4 bytes float
        encoded_data.append(self.prop_temp_1.to_bytes(4, 'little')) # 4 bytes float
        encoded_data.append(self.prop_temp_2.to_bytes(4, 'little')) # 4 bytes float
        encoded_data.append(self.prop_power_i_1.to_bytes(4, 'little')) # 4 bytes float
        encoded_data.append(self.prop_power_i_2.to_bytes(4, 'little')) # 4 bytes float
        encoded_data.append(self.prop_power_v_1.to_bytes(4, 'little')) # 4 bytes float
        encoded_data.append(self.prop_power_v_2.to_bytes(4, 'little')) # 4 bytes float
        return encoded_data

# ADCS data
#class AdcsData(Data):
    # ...

class CommsMainTask(Task):
    mode = CommsModes.SCANNING

    logged_data = []

    def encode_data(self, data):
        for datapoint in data:
            encoded_data = datapoint.encode()
        return encoded_data

    def send_data(self, data):
        io_transmit_data(data)
    
    def is_enough_logged_data(self):
        return logged_data > 10

    async def main_task(self):
        match self.mode:
            case CommsModes.SCANNING:
                print("scanning")
                if io_is_receiving_beacon():
                    # if beacon is received, transition to TRASNMITTING mode
                    self.mode = CommsModes.TRANSMITTING

            case CommsModes.TRANSMITTING:
                print("transmitting")
                datapoint_1 = PropData()
                datapoint_1.prop_press_1 = 1
                self.logged_data.append(datapoint_1)
                
                # encode the data
                encoded_data = self.encode_data(self.logged_data)

                # encrypt the data
                # perform data encoding that Kelanu (aka. Thanos) will determine
                # ... TBD

                # transmit the data
                io_transmit_data(encoded_data)

                # end of transmission, go back to scanning
                self.mode = CommsModes.SCANNING

        # encode data
        # truncate data
        # send to ground station
        # send EOF completition