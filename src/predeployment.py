import time
import board
from adafruit_extended_bus import ExtendedI2C as I2C
import adafruit_bno055
import adafruit_bmp3xx

i2c = I2C(5)  # uses board.SCL and board.SDA
bno = adafruit_bno055.BNO055_I2C(i2c)
bmp = adafruit_bmp3xx.BMP3XX_I2C(i2c)

class sensor:
    
	@property #return integral 
	def integrate(self, data: list[any]) -> any:
		pass
	
	@property #return averaged derivative
	def differentiate(self, data: list[any]) -> any:
		pass

class Alt(sensor):
	def __init__(self, imu, groundAlt: float, apogee: float):
		self.alt = alt
		self.groundAlt = groundAlt
		self.apogee = apogee
	
	@property #averaged altitude from sensor
	def altitude(self, samples: int) -> float:
		return self.alt.altitude

	@property #averaged differentiation of altitude -> velocity
	def velocity(self, samples: int) -> float:
		pass

class IMU(sensor):
	def __init__(self, imu, launchVelocity: float) -> None:
		self.imu = imu  
		self.launchVelocity = launchVelocity
 
	@property #averaged acceleration
	def acceleration(self, samples: int) -> tuple[float, float, float]:
		return self.imu.acceleration    

	@property #averaged integration of acceleration -> velocity
	def velocity(self, samples: int) -> tuple[float, float, float]:
		pass

	
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
    
