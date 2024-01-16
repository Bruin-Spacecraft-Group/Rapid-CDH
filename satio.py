# handles fake IO n stuff
# in the end, we should replace this with actual stuff, idk what yet

import random

# poll is received beacon?

def io_is_receiving_beacon():
    return True

def io_transmit_data(data):
    print('comms is transmitting data', data)