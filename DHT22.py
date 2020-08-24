#!/usr/bin/python
import Adafruit_DHT
import RPi.GPIO as GPIO
import time
import board
import neopixel


import requests
import json

import lcddriver


    sensor = Adafruit_DHT.DHT22
    pin = 22
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
    temperatur = '{0:0.1f}'.format(temperature)
    feuchtigkeit = '{0:0.1f}%'.format(humidity)
    print("Temperatur_DHT22: ", temperatur)
    print("Feuchtigkeit_DHT22: ",feuchtigkeit)
