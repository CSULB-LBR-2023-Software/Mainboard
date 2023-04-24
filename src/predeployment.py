#! /usr/bin/env python3

import RPi.GPIO as GPIO
import time

# PIN DEFS
GIMB_LAUNCH = 8
GIMB_LAND = 11
DEPL_LAUNCH = 18
DEPL_COMPLETE = 21


def setup_inputs(*pins: int) -> None:
    GPIO.setmode(GPIO.BCM)
    for pin in pins:
        GPIO.setup(pin, GPIO.IN)

if __name__ == "__main__":
    setup_inputs(GIMB_LAND, GIMB_LAUNCH, DEPL_LAUNCH, DEPL_COMPLETE)
    state = lambda port : GPIO.input(port)

    try:
        while not (state(GIMB_LAUNCH) and state(DEPL_LAUNCH)):
            continue
        print("Launch detected.")
        while not state(GIMB_LAND):
            continue
        print("Landed detected,")
        while not state(DEPL_COMPLETE):
            continue
        print("Deployment detected, proceeding to deployment.")
        GPIO.cleanup()
    except KeyboardInterrupt:
        GPIO.cleanup()
        print()

