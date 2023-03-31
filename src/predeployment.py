#! /usr/bin/env python3

import adafruit_bmp3xx
import adafruit_bno055
import board
import numpy as np
import sys
import time 

from adafruit_extended_bus import ExtendedI2C as I2C
from math import pow, sqrt
from state_machine import States, StateMachine


# CONSTANTS
SENSOR_I2C_BUS = 5  #using I2C bus 5
FILE_NAME = "missionStates"
PATH = f"./{FILE_NAME}.json"


class IMU:
    "I2C BNO055 sensor poller."""

    def __init__(self, imu: adafruit_bno055.BNO055_I2C) -> None:
        """Creates a new IMU sampler using an I2C BNO055 object."""
        self.imu = imu

    def linear_accel(self, samples: int, averaged: bool=True) -> np.array:
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

    def altitude(self, samples: int, averaged: bool=True) -> np.array:
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

def majority_bool(*bool_args: bool) -> bool:
    """Checks whether bool arguments are majority True.

    Args:
        *bool_args(bool): var args for any number of bool values
    
    Returns:
        bool: True if majority of parameters are True, otherwise False
    """
    bools = [x for x in bool_args]
    return bools.count(True) > (len(bools) / 2)

if __name__ == "__main__":
    # state machine setup
    states = StateMachine(PATH)
    states.setNewState(States.PREDEPLOYMENT, States.PREDEPLOYMENT_SUBS)
    print(f"State: {states.getState()} | Substate: {states.getSubstate()}")
    print(states)
    
    # sensor setup
    imu, baro = setup(SENSOR_I2C_BUS)
    
    # launch check
    acc = imu.linear_accel(100)
    alt = baro.altitude(100)
    while not vector_mag(acc) > 35 and not alt > 100:
        print(f"Linear Acc: {vector_mag(acc)} | Alt: {alt}")
        acc = imu.linear_accel(100)
        alt = baro.altitude(100)
    states.updateState(States.PREDEPLOYMENT, "Launch", True)
    
    # land check  
    while not vector_mag(acc) < 2 and not alt > 20:
        print(f"Linear Acc: {vector_mag(acc)} | Alt: {alt}")
        acc = imu.linear_accel(100)
        alt = baro.altitude(100)
    states.updateState(States.PREDEPLOYMENT, "Land", True)

    states.setNewState(States.DEPLOYMENT, States.DEPLOYMENT_SUBS)
    


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
