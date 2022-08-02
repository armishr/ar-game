# -*- coding: utf-8 -*-
"""
Created on Tue Aug  2 19:36:18 2022

@author: Adithya Raj Mishra
"""
import serial

#can read gyro values successfully
ser = serial.Serial('COM3',9600)
print((float)(ser.readline().decode().rstrip().split()[0]) + 1)
print(ser.readline().decode().rstrip())
print(ser.readline().decode().rstrip())
print(ser.readline().decode().rstrip())
print(ser.readline().decode().rstrip())
print(ser.readline().decode().rstrip())
print(ser.readline().decode().rstrip())
print(ser.readline().decode().rstrip())
ser.close()