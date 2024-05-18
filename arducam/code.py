#============= Imports =============

# pip3 install circup
# circup install adafruit_ov5640
# circup update

import time

import board
import busio
import digitalio

import adafruit_ov5640

#============= Setting Up Output =============
switch=digitalio.DigitalInOut(board.D2) # Replace D2 with proper pin
switch.switch_to_input()

if switch.value==True: # if pin is pulled high, then datalog mode -- no USB write allowed
    try:
        with open('/data.txt','ab') as f:
            pass
    except OSError as e:
        print ("BRUH")

#============= Connect to Camera =============

bus = busio.SPI(clock=board.GP2, MOSI=board.GP3, MISO=board.GP4) # Replace GP2, GP3, GP4 with proper pins
cam = adafruit_ov5640.OV5640(
    bus,
    data_pins=board.CAMERA_DATA,
    clock=board.CAMERA_PCLK,
    vsync=board.CAMERA_VSYNC,
    href=board.CAMERA_HREF,
    mclk=board.CAMERA_XCLK,
    size=adafruit_ov5640.OV5640_SIZE_QSXGA,
)

#============= Take Pic =============

cam.colorspace = adafruit_ov5640.OV5640_COLOR_JPEG
cam.quality = 5
b = bytearray(cam.capture_buffer_size)
print(f"Capturing jpeg image of up to {len(b)} bytes")
jpeg = cam.capture(b)

#============= Write to Output =============

print(f"Captured {len(jpeg)} bytes of jpeg data")
try:
    print(end="Writing to internal storage (this is SLOW)")
    with open("/cam.jpg", "wb") as f:
        for i in range(0, len(jpeg), 4096):
            print(end=".")
            f.write(jpeg[i : i + 4096])
    print()
    print("Wrote to /cam.jpg")
    time.sleep(0.5)

except OSError as e:
    print(e)
    print("BRUH")


