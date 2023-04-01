
#! /usr/bin/env python3

import RPi.GPIO as GPIO
import time

# PIN DEFS
# high 10 ms low for 3 seconds
PIN1 = 17 # BC pin 17, P1 pin 11
PIN2 = 18

def setup_inputs(*pins: int) -> None:
    GPIO.setmode(GPIO.BCM)
    for pin in pins:
        GPIO.setup(pin, GPIO.IN)

if __name__ == "__main__":
    pin1 = PIN1
    pin2 = PIN2
    setup_inputs(pin1)

    try:
        while not GPIO.input(pin1) and GPIO.input(pin2):
            continue
        print("Signal detected, proceeding to deployment.")

    except KeyboardInterrupt:
        GPIO.cleanup()
        print()
