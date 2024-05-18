import digitalio
import board
import storage

switch=digitalio.DigitalInOut(board.D2) # Replace D2 with proper pin
switch.switch_to_input()

storage.remount("/", not switch.value) # switch.value==False means datalogging mode:  allow circuitpython code to write to flash, while making USB read-only.  So: pull pin high for datalogging, leave pin at ground for USB write access (reprogramming).