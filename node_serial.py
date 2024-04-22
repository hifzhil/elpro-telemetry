#!/usr/bin/env python3
import time
import serial
from paho.mqtt import client as mqtt_client


class SerialData(object) :
	def __init__(self):
		self.ser_ = serial.Serial( port='COM6',
								baudrate = 9600,
								parity=serial.PARITY_NONE,
								stopbits=serial.STOPBITS_ONE,
								bytesize=serial.EIGHTBITS,
								timeout=1)
		self.mcu_data_str_ = ""
		self.speed_data = 0
		self.rpm_data = 0
		self.temp_data = 0
		self.limiter_data = 0
	def callback(self, data) :
		self.mcu_data_str_ = data.decode('utf-8')
		print(self.mcu_data_str_)
	def update(self):
		ser_data=self.ser_.readline().strip()
		if len(ser_data) >=16 :
			self.callback(ser_data)

	def get_data(self):
		return self.mcu_data_str_