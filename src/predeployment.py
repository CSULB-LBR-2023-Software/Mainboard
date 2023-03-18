import time
import board
from adafruit_extended_bus import ExtendedI2C as I2C
import adafruit_bno055
import adafruit_bmp3xx

i2c = I2C(5)  # uses board.SCL and board.SDA
bno = adafruit_bno055.BNO055_I2C(i2c)
bmp = adafruit_bmp3xx.BMP3XX_I2C(i2c)

class sensor:
    def integration(self, data):

class IMU(sensor):
    def __init__(self, imu):
        self.imu = imu
    
    def acceleration(self):
        return self.imu.acceleration    

imu = IMU(bno)

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
    
