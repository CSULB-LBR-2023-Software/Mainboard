import time
import numpy as np

import board
import adafruit_bno055
import adafruit_bmp3xx

i2c = board.I2C() 
imu = adafruit_bno055.BNO055_I2C(i2c)
alt = adafruit_bmp3xx.BMP3XX_I2C(i2c)

def printout():
    print("Accelerometer (m/s^2): {}".format(imu.acceleration))
    print("Magnetometer (microteslas): {}".format(imu.magnetic))
    print("Gyroscope (rad/sec): {}".format(imu.gyro))
    print("Euler angle: {}".format(imu.euler))
    print("Quaternion: {}".format(imu.quaternion))
    print("Linear acceleration (m/s^2): {}".format(imu.linear_acceleration))
    print("Gravity (m/s^2): {}".format(imu.gravity))
    print("Pressure: {:6.4f}  Temperature: {:5.2f}".format(alt.pressure, alt.temperature))

def average(sensor, samples):
    total = (0, 0, 0)
    for x in range(samples):
        total += np.add(total, imu.acceleration)
    
    return total / samples

while True:
    
    averageAcceleration = average(imu, 5)
    print(averageAcceleration)
    time.sleep(1)