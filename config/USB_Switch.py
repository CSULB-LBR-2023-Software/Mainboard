import RPi.GPIO as gpio
import time
import sys

#define pins and states 
DISABLE = True
ENABLE = False
SWITCH_STATE = None
SWITCH_PIN = 6

#setup 
gpio.setwarnings(False)
gpio.cleanup()
gpio.setmode(gpio.BCM)
gpio.setup(SWITCH_PIN, gpio.OUT)

#set usb switch based on input argument
if sys.argv[1] == "-e":
    SWITCH_STATE = ENABLE

elif sys.argv[1] == "-d":
    SWITCH_STATE = DISABLE


while True:
    gpio.output(SWITCH_PIN, SWITCH_STATE);
