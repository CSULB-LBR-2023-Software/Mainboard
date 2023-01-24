import time
import numpy as np
from scipy import integrate

import board
import adafruit_bno055
import adafruit_bmp3xx


APOGEE = 1371 #4500 ft 
LAUNCH_ALT_THRESH = 10
LAUNCH_VELOCITY_THRESH = (1, 1, -15)
LAND_ALT_THRESH = 10
LAND_LIN_ACC_THRESH = (0.25, 0.25, 0.25)

LaunchFlag = False
ApogeeFlag = False
DescentFlag = False
LandAltFlag = False
LandLinAccFlag = False
LandFlag = False

i2c = board.I2C() 
imu = adafruit_bno055.BNO055_I2C(i2c)
alt = adafruit_bmp3xx.BMP3XX_I2C(i2c)


class SensorTools:
    def __init__(self, i2c, imu, alt):
        self.i2c = i2c
        self.imu = imu
        self.alt = alt
        self.groundAlt = self.average(self.alt, "altitude", 10)

    def average(self, sensor, value, samples):
        total = []
        for x in range(samples):
            total.append(getattr(sensor, value))

        #filter None that can ocasionally return from IMU    
        total = list(filter((None, None, None).__ne__, total))
        return np.average(total, axis = 0)

    def differentiate(self, sensor, value, samples):
        data = []
        t = []

        data.append(self.average(sensor, value, round(samples / 2)))
        t.append(time.time())

        data.append(self.average(sensor, value, round(samples / 2)))
        t.append(time.time())

        return np.gradient(data, t)

    def integrate(self, sensor, value, samples):
        for x in range(samples):
            sample = []
            t = []

            sample.append(getattr(sensor, value))  
            t.append(time.time())        
        
        return integrate.simpson(sample, t)

#Pre-launch checks
sensor = SensorTools(i2c, imu, alt)
while True: 

    #break if altitude and acceleration threshold exceeded
    if sensor.average(alt, "altitude", 10) < sensor.groundAlt + LAUNCH_ALT_THRESH:
        continue

   
    if  sensor.integrate(imu, "acceleration", 10) < LAUNCH_VELOCITY_THRESH: 
        continue

    break

LaunchFlag = True


#Apogee and descent checks
while True:
    #break if apogee detected
    if sensor.average(alt, "altitude", 10) > sensor.groundAlt + APOGEE:
        ApogeeFlag = True
        break

    #break if altitude is descending

    if sensor.differentiate(alt, "altitude", 10) < 0:
        DescentFlag = True
        break


#Landed checks 
while True:

    #break if below ground and acceleration landing thresholds     
    if sensor.average(alt, "altitude", 50) > sensor.groundAlt + LAND_ALT_THRESH:
        continue
    
    if sensor.average(imu, "linear_acceleration", 50) > LAND_LIN_ACC_THRESH:
        continue

    break

LandFlag = True