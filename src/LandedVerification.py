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
    total = []
    for x in range(samples):
        total.append(getattr(sensor, value))
    
    total = list(filter((None, None, None).__ne__, total))
    return np.average(total, axis = 0)



def decreasing(sensor, value, samples):

    total = []
    timestamp = []
    for x in range(samples):
        start = time.time()
        
        sample = getattr(sensor, value)

        total.append(sample)
        timestamp.append(time.time() - start)
    
    #first derivative
    dydx = diff(total) / diff(x)
    return dydx
        






#groundAlt = average(alt, "pressure", 10)
#while( (average(alt, "pressure", 10) < 10) and (average(imu.linear_acceleration) < (5, 5, 5)))
#LaunchedFlag = 1

while True: 
    decreasing(alt, "pressure", 100)
    time.sleep(1)


