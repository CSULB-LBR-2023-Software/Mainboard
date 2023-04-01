#! /usr/bin/env python3

import adafruit_bmp3xx
import adafruit_bno055
import numpy as np
import os
import sys
import time

from adafruit_extended_bus import ExtendedI2C as I2C
from collections import Counter
from math import pow, sqrt
from state_machine import States, StateMachine


# CONSTANTS
SENSOR_I2C_BUS = 5  #using I2C bus 5
FILE_NAME = "missionStates"
PATH = f"./{FILE_NAME}.json"

SAMPLES = 100
LIN_ACCEL_CEILING = 12 # 35
LIN_ACCEL_FLOOR = 2
ALT_CEILING = 0 # 100
ALT_FLOOR = 20


class IMU:
    "I2C BNO055 sensor poller."""

    def __init__(self, imu: adafruit_bno055.BNO055_I2C) -> None:
        """Creates a new IMU sampler using an I2C BNO055 object."""
        self.imu = imu

    def linear_accel(self, samples: int, averaged: bool=True) -> np.ndarray:
        """Polls acceleration samples and returns the average.

        Args:
            samples(int): the number of samples to take

        Returns:
            np.array: the array of averaged data
        """
        ret = np.zeros([samples, 3])
        for i in range(samples):
            data = self.imu.acceleration
            while None in data:
                data = self.imu.acceleration
            ret[i] = data
        if averaged:
            return np.mean(ret, axis=0)
        return ret

class BARO:
    "I2C BMP390 sensor poller."

    def __init__(self, baro: adafruit_bmp3xx.BMP3XX_I2C, ground: int) -> None:
        """Creates a new BMP sampler using an I2C BMP390 object."""
        self.baro = baro
        self.ground = ground

    def altitude(self, samples: int, averaged: bool=True) -> np.ndarray:
        """Polls altitude samples and returns the average."""
        ret = np.zeros([samples, 1])
        for i in range(samples):
            data = self.baro.altitude
            while not data:
                data = self.baro.altitude - self.ground
            ret[i]
        if averaged:
            return np.mean(ret)
        return ret

def setup(bus: int, ground: int = None) -> tuple:
    """Returns tuple of initialized IMU, Baro.

    Args:
        bus(int): the sensor I2C bus
        ground(int): baro ground reference
    """
    i2c = I2C(bus)
    bno = adafruit_bno055.BNO055_I2C(i2c)
    bmp = adafruit_bmp3xx.BMP3XX_I2C(i2c)
    imu = IMU(bno)
    if not ground:
        ground = bmp.altitude
    baro = BARO(bmp, ground)
    return imu, baro

def vector_mag(vector: np.ndarray) -> int:
    """Returns the vector magnitude of an array of values.

    Args:
        vector(np.ndarray): the vector to take the magnitude of
    """
    return sqrt(sum(pow(val, 2) for val in vector))

def majority(*args) -> object:
    """Checks for majority elements.

    ** MAKE SURE TO PASS MOST RELIABLE OBJECT FIRST, IE STM

    Args:
        *args: Var args for any number of variables

    Returns:
        object: The most common element, or the first passed element
        if there is no most common
    """
    vars = Counter([x for x in args])
    return vars.most_common(1)[0][0]

def pollSTMSubstate(uc) -> str:
    "DEBUGGING"
    return States.Substates.RAIL

def checkPiState(samples: int, rail: bool) -> str:
    acc = imu.linear_accel(samples)
    alt = baro.altitude(samples)
    if not rail:
        accAvg = vector_mag(acc)
        if not accAvg > LIN_ACCEL_CEILING and not alt > ALT_CEILING:
            return States.Substates.LAUNCH
        return States.Substates.RAIL
    else:
        if not vector_mag(acc) < LIN_ACCEL_FLOOR and not alt > ALT_FLOOR:
            return States.Substates.LAND
        return States.Substates.LAUNCH


if __name__ == "__main__":
    # state machine setup
    if not os.path.exists(PATH):
        states = StateMachine(PATH)
        states.setNewState(States.PREDEPLOYMENT, States.PREDEPLOYMENT_SUBS)
    else:
        states = StateMachine(PATH)
        json = (states.getSubstate())
        maj_states = majority(json)
        if maj_states in States.DEPLOYMENT_SUBS.keys():
            print("Exit Deployment")
            sys.exit(2)
        if maj_states in States.MISSION_SUBS.keys():
            print("Exit mission")
            sys.exit(3)
        if maj_states in States.PREDEPLOYMENT_SUBS.keys():
            print("Continuing Predeployment")

    print(f"State: {states.getState()} | Substate: {states.getSubstate()}")
    #print(states)

    rail = False

    # sensor setup
    imu, baro = setup(SENSOR_I2C_BUS)

    # check launch
    if pollSTMSubstate("stmID") is States.Substates.RAIL:
        rail = True
        print("On Rail")
        vote = majority(pollSTMSubstate("stmID"), pollSTMSubstate("stmID"), checkPiState(SAMPLES, rail))
        while vote is not States.Substates.LAUNCH:
            vote = majority(pollSTMSubstate("stmID"), pollSTMSubstate("stmID"), checkPiState(SAMPLES, rail))
            print(vote)
        states.updateState(States.PREDEPLOYMENT, vote, True)
        print("Launch detected")
        rail = False

    # check land
    print(states)

    vote = majority(pollSTMSubstate("stmID"), pollSTMSubstate("stmID"), checkPiState(SAMPLES, rail))
    while vote is not States.Substates.LAND:
        vote = majority(pollSTMSubstate("stmID"), pollSTMSubstate("stmID"), checkPiState(SAMPLES, rail))
    states.updateState(States.PREDEPLOYMENT, vote, True)
    print("Land detected")

    #states.setNewState(States.DEPLOYMENT, States.DEPLOYMENT_SUBS)
    print("Exit for deployment")
    print("Make sure to set deployment state at beginning of deployment file.")
    sys.exit(2)

    #print(states)


    """
    avg = bool(int(sys.argv[2]))
    samples = int(sys.argv[1])
    print("Setup done")
    start = time.perf_counter()
    avgAccel = imu.linear_accel(samples, averaged=avg)
    avgAlt = baro.altitude(samples, averaged=avg)
    print(time.perf_counter() - start)
    print(f"Accel: {avgAccel}")
    print(f"Alt: {avgAlt}")
    """