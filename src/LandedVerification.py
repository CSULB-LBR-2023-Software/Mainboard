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

def average(sensor, value, samples):
   
    try:
        total = []
        for x in range(samples):
            total.append(getattr(sensor, value))

        return np.average(total, axis = 0)

    except TypeError:
        total = list(filter((None, None, None).__ne__, total))
        return np.average(total, axis = 0)

def decreasing(sensor, value, samples):
    x = 0
    while(x < 1000):
        
        sample1 = []
        sample2 = []

        sample1 = average(sensor, value, samples)
        sample2 = average(sensor, value, samples)

        difference = np.subtract(sample1, sample2)
        
        if(difference < 0):
            x += 1



while True:
    start = time.time()
    print(average(imu, "acceleration", 500))
    end = time.time() - start
    print("Time: {} \n".format(end))
    
    start = time.time()
    print(average(alt, "pressure", 500))
    end = time.time() - start
    print("Time: {} \n".format(end))


    time.sleep(1)
