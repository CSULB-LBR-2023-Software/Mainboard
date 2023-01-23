import time
import numpy as np

import board
import adafruit_bno055
import adafruit_bmp3xx


APOGEE = 1371 #4500 ft 
LAUNCH_ALT_THRESH = 10
LAUNCH_LIN_ACC_THRESH = 3
LAND_ALT_THRESH = 10
LAND_LIN_ACC_THRESH = 1

LaunchedFlag = False
ApogeeFlag = False
DescentFlag = False

LandAltFlag = False
LandLinAccFlag = False
LandedFlag = False

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


#Pre-launch checks
groundAlt = average(alt, "altitude", 10)

while True: 

    if average(alt, "altitude", 10) < groundAlt + LAUNCH_ALT_THRESH:
        continue

    if average(imu, "linear_acceleration", 10) < np.fill((1, 3), LAUNCH_LIN_ACC_THRESH):
        continue

    break

LaunchedFlag = True


#Apogee and descent checks
while True:
    #check for apogee
    if average(alt, "altitude", 10) < groundAlt + APOGEE:
        ApogeeFlag = True
        break

    #check for descent
    y = []
    x = []
    y.append(average(alt, "altitude", 10))
    x.append(time.time())
    y.append(average(alt, "altitude", 10))
    x.append(time.time())

    dydx = (diff(y)/diff(x))[0]

    if dydx < 0 :
        DescentFlag = True
        break


#Landed checks 
while True:
    
    if average(alt, "altitude", 50) > groundAlt + LAND_ALT_THRESH:
        continue
    
    if average(imu, "linear_acceleration", 50) > np.fill((1, 3), LAND_LIN_ACC_THRESH):
        continue

    break

LandedFlag = True

    


