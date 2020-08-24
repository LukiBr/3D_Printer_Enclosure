#!/usr/bin/python
import Adafruit_DHT
import RPi.GPIO as GPIO
import time
import board
import neopixel


import requests
import json





'''
DHT-22 Luft- und Feuchtigkeitssensor
'''
def dht22_luftfeuchtigkeit():
    sensor = Adafruit_DHT.DHT22
    pin = 22
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
    temperatur = '{0:0.1f}'.format(temperature)
    feuchtigkeit = '{0:0.1f}%'.format(humidity)
    print("Temperatur_DHT22: ", temperatur)
    print("Feuchtigkeit_DHT22: ",feuchtigkeit)
    return (temperatur, feuchtigkeit)

'''
Temperatursensor
'''
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


'''
Lüftersteuerung
'''
#Globale Variablen
# Relais GPIO Singal
channel = 17

# Temperatur ab der die Lüfter los legen (Grad)
temperatur_index = 20



# GPIO setup
#GPIO.setmode(GPIO.BCM)
#GPIO.setup(channel, GPIO.OUT)

def luefter_an(pin):
    channel = 17
    GPIO.output(pin, GPIO.HIGH)
    zustand = "Lüfter an"
    print(zustand)

def luefter_aus(pin):
    channel = 17
    GPIO.output(pin, GPIO.LOW)
    zustand = "Lüfter aus"
    print(zustand)

def luefter_steuerung():
    # GPIO setup
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(channel, GPIO.OUT)

    temp = ds18b20_temp_sensor()
    print(temp)
    if temp > temperatur_index:
        luefter_an(channel)
        time.sleep(10)
    else:
        luefter_aus(channel)
        time.sleep(10)


'''
WS2812 LED-Stripe
'''
def ws2812_weis():
    #Board-PIN, Anzahl der LEDs
    pixels = neopixel.NeoPixel(board.D18, 60)

    #gesamter Streifen
    pixels.fill((252, 252, 252))

def ws2812_rot():
    #Board-PIN, Anzahl der LEDs
    pixels = neopixel.NeoPixel(board.D18, 60)

    #gesamter Streifen
    pixels.fill((255, 0, 0))

def ws2812_grün():
    #Board-PIN, Anzahl der LEDs
    pixels = neopixel.NeoPixel(board.D18, 60)

    #gesamter Streifen
    pixels.fill((0, 255, 0))

def ws2812_blau():
    #Board-PIN, Anzahl der LEDs
    pixels = neopixel.NeoPixel(board.D18, 60)

    #gesamter Streifen
    pixels.fill((0, 0, 255))






def main():
    while True:

        dht22_luftfeuchtigkeit()
        ds18b20_temp_sensor()
        luefter_steuerung()
        ws2812_weis()
        temperatur, feuchtigkeit = dht22_luftfeuchtigkeit()
        temp = str(ds18b20_temp_sensor())
        print(temp)
        print(temperatur)
        print(feuchtigkeit)




if __name__ == '__main__':
    main()

