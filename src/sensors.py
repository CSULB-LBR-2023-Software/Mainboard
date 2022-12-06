# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time
import board
import adafruit_bmp3xx


class BMP:

	'''
	Adafruit BMP390 object to return altimeter data
	'''

	def __init__(self):
		self.i2c = board.I2C()
		self.bmp = adafruit_bmp3xx.BMP3XX_I2C(self.i2c)
		self.bmp.pressure_oversampling = 8
		self.bmp.temperature_oversampling = 2

	def alt(self):
		return self.bmp.altitude

	def __str__(self):
		s = f"Temp: {self.bmp.temperature}, Pressure: {self.bmp.pressure}, \
			Alt: {self.bmp.altitude}"
		return s


class IMU:

	'''
	Adafruit BNO55 object to return orientation data
	'''

	def __init__(self):
		pass
