#!/usr/bin/python
import Adafruit_DHT
import RPi.GPIO as GPIO
import time
import board
import neopixel


import requests
import json


# Temperatur ab der die Lüfter los legen (Grad)
temperatur_index = 20

pin = 17

'''
Temperatursensor
'''

def setup():
    # GPIO setup
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin, GPIO.OUT)

def ds18b20_temp_sensor():
    file = open('/sys/bus/w1/devices/28-0416a0d4a1ff/w1_slave')
    filecontent = file.read()
    file.close()
    # Temperaturwerte auslesen und konvertieren
    stringvalue = filecontent.split("\n")[1].split(" ")[9]
    temperature = float(stringvalue[2:]) / 1000
    print("Temperatur_DS18b20:", temperature)
    # Temperatur ausgeben
    # rueckgabewert = '%6.2f' % temperature
    return (temperature)

def luefter_an(pin):
    GPIO.output(pin, GPIO.HIGH)
    zustand = "Lüfter an"
    print(zustand)

def luefter_aus(pin):
    GPIO.output(pin, GPIO.LOW)
    zustand = "Lüfter aus"
    print(zustand)

def luefter_steuerung():
    temp = ds18b20_temp_sensor()
    print(temp)
    if temp > temperatur_index:
        luefter_an(pin)
        time.sleep(10)
    else:
        luefter_aus(pin)
        time.sleep(10)


def main():
    setup()
    while True:
        luefter_steuerung()
        #temp = str(ds18b20_temp_sensor())
        #print(temp)



if __name__ == '__main__':
    main()

