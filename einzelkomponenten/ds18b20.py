#!/usr/bin/python
import Adafruit_DHT
import RPi.GPIO as GPIO
import time
import board
import neopixel


import requests
import json


file = open('/sys/bus/w1/devices/28-0416a0d4a1ff/w1_slave')
filecontent = file.read()
file.close()
# Temperaturwerte auslesen und konvertieren
stringvalue = filecontent.split("\n")[1].split(" ")[9]
temperature = float(stringvalue[2:]) / 1000
print("Temperatur_DS18b20:", temperature)
# Temperatur ausgeben
# rueckgabewert = '%6.2f' % temperature
