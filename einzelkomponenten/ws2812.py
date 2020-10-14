#!/usr/bin/python
import Adafruit_DHT
import RPi.GPIO as GPIO
import time
import board
import neopixel


import requests
import json

#Board-PIN, Anzahl der LEDs
pixels = neopixel.NeoPixel(board.D18, 60)
#gesamter Streifen
pixels.fill((252, 252, 252))
