import time
import board

from adafruit_extended_bus import ExtendedI2C as I2C
import adafruit_bno055
import adafruit_bmp3xx

import numpy as np

SENSOR_I2C_BUS = 5 #using I2C bus 5

i2c = I2C(SENSOR_I2C_BUS)  
bno = adafruit_bno055.BNO055_I2C(i2c)
bmp = adafruit_bmp3xx.BMP3XX_I2C(i2c)

class sensor:
	#return integral 
	def integrate(self, data: list[any]) -> any:
		pass
	
	#return averaged derivative
	def differentiate(self, data: list[any]) -> any:
		pass
		
	def sample(self, function: any, samples: int) -> list[float]:
		data = []

		for x in range(samples):
			data.append(function)

		return data

class Alt(sensor):
	def __init__(self, imu, groundAlt: float, apogee: float) -> None:
		self.alt = alt
		self.groundAlt = groundAlt
		self.apogee = apogee
	
	#averaged altitude from sensor
	def altitude(self, samples: int) -> float:
		altitude = self.sample(self.alt.altitude, samples)
		averageAlt = np.average(altitude)
		return averageAlt		

	#averaged differentiation of altitude -> velocity
	def velocity(self, samples: int) -> float:
		altitude = self.sample(self.alt.altitude, samples)
		velocity = self.differentiate(altitude)
		average = np.average(velocity)
		return averageVelocity	


class IMU(sensor):
	def __init__(self, imu, launchVelocity: float) -> None:
		self.imu = imu  
		self.launchVelocity = launchVelocity
 
	#averaged acceleration
	def acceleration(self, samples: int) -> tuple[float, float, float]:
		accel = self.sample(self.imu.acceleration, samples)
		averageAccel = np.average(accel)
		return averageAccel

	#integration of acceleration -> velocity
	def velocity(self, samples: int) -> tuple[float, float, float]:
		accel = self.sample(self.imu.acceleration, samples)	
		velocity = integrate(accel)
		return velocity


	
imu = IMU(bno)
alt = Alt(bmp)

while True:
    '''
    print("Accelerometer (m/s^2): {}".format(sensor.acceleration))
    print("Magnetometer (microteslas): {}".format(sensor.magnetic))
    print("Gyroscope (rad/sec): {}".format(sensor.gyro))
    print("Euler angle: {}".format(sensor.euler))
    print("Quaternion: {}".format(sensor.quaternion))
    print("Linear acceleration (m/s^2): {}".format(sensor.linear_acceleration))
    print(
        "Altitude: {:6.4f} Pressure: {:6.4f}".format(bmp.altitude, bmp.pressure)
    )
    print()

    time.sleep(1)
    '''
    
    print(imu.acceleration)
    time.sleep(1)
    
