
#!/usr/bin/python3

import time
import RPi.GPIO as GPIO

#Display
import datetime
import smbus
import socket
import os
import sys


#Relais GPIO Singal
channel = 17

#Temperatur ab der die Lüfter los legen (Grad)
temperatur_index = float(20)

# GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(channel, GPIO.OUT)


def aktuelleTemperatur():

    # 1-wire Slave Datei lesen
    file = open('/sys/bus/w1/devices/28-0416a0d4a1ff/w1_slave')
    filecontent = file.read()
    file.close()

    # Temperaturwerte auslesen und konvertieren
    stringvalue = filecontent.split("\n")[1].split(" ")[9]
    temperature = float(stringvalue[2:]) / 1000
    print(temperature)
    # Temperatur ausgeben
    #rueckgabewert = '%6.2f' % temperature
    #return(rueckgabewert)
    return(temperature)


def luefter_an(pin):
    GPIO.output(pin, GPIO.HIGH)
    zustand = "Lüfter an"
    print("Lüfter an")

def luefter_aus(pin):
    GPIO.output(pin, GPIO.LOW)
    zustand = "Lüfter aus"
    print("Lüfter an")


# Define some device parameters
I2C_ADDR  = 0x27 # I2C device address
LCD_WIDTH = 16   # Maximum characters per line

# Define some device constants
LCD_CHR = 1 # Mode - Sending data
LCD_CMD = 0 # Mode - Sending command
LCD_LINE_1 = 0x80 # LCD RAM address for the 1st line
LCD_LINE_2 = 0xC0 # LCD RAM address for the 2nd line
LCD_LINE_3 = 0x94 # LCD RAM address for the 3rd line
LCD_LINE_4 = 0xD4 # LCD RAM address for the 4th line

LCD_BACKLIGHT  = 0x08  # On
#LCD_BACKLIGHT = 0x00  # Off

ENABLE = 0b00000100 # Enable bit

# Timing constants
E_PULSE = 0.0005
E_DELAY = 0.0005

#Open I2C interface
#bus = smbus.SMBus(0)  # Rev 1 Pi uses 0
bus = smbus.SMBus(1) # Rev 2 Pi uses 1

def lcd_init():
    # Initialise display
    lcd_byte(0x33,LCD_CMD) # 110011 Initialise
    lcd_byte(0x32,LCD_CMD) # 110010 Initialise
    lcd_byte(0x06,LCD_CMD) # 000110 Cursor move direction
    lcd_byte(0x0C,LCD_CMD) # 001100 Display On,Cursor Off, Blink Off
    lcd_byte(0x28,LCD_CMD) # 101000 Data length, number of lines, font size
    lcd_byte(0x01,LCD_CMD) # 000001 Clear display
    time.sleep(E_DELAY)

def lcd_byte(bits, mode):
# Send byte to data pins
# bits = the data
# mode = 1 for data
#        0 for command

    bits_high = mode | (bits & 0xF0) | LCD_BACKLIGHT
    bits_low = mode | ((bits<<4) & 0xF0) | LCD_BACKLIGHT

    # High bits
    bus.write_byte(I2C_ADDR, bits_high)
    lcd_toggle_enable(bits_high)

    # Low bits
    bus.write_byte(I2C_ADDR, bits_low)
    lcd_toggle_enable(bits_low)

def lcd_toggle_enable(bits):
    # Toggle enable
    time.sleep(E_DELAY)
    bus.write_byte(I2C_ADDR, (bits | ENABLE))
    time.sleep(E_PULSE)
    bus.write_byte(I2C_ADDR,(bits & ~ENABLE))
    time.sleep(E_DELAY)

def lcd_string(message,line):
# Send string to display
    message = message.ljust(LCD_WIDTH," ")
    lcd_byte(line, LCD_CMD)
    for i in range(LCD_WIDTH):
        lcd_byte(ord(message[i]),LCD_CHR)





while True:
    lcd_init()
    temp = aktuelleTemperatur()
    print(temp)
    if temp > temperatur_index:
        luefter_an(channel)
        time.sleep(10)
    else:
        luefter_aus(channel)
        time.sleep(10)

    #Umwandlung für Display
    temp_display = str(temp)

    #Ip-Adressen der Geräte
    ipadresse_octoprint = "192.168.2.21"
    ipadresse_raspberry = "192.168.2.22"
    ipadresse_esp8266 = "192.168.2.93"

    #Datum und Uhrzeit
    value1data =time.strftime("%d.%m.%Y")
    value2data =time.strftime("%H:%M")
    
    #Send some test
    lcd_string("Temperatur:",LCD_LINE_1)
    lcd_string(temp_display + " Grad",LCD_LINE_2)

    time.sleep(10)

    # Send some more text
    lcd_string("IP-Adresse:",LCD_LINE_1)
    lcd_string(ipadresse_esp8266,LCD_LINE_2)

    time.sleep(10)

    # Send some more text
    lcd_string("Datum:",LCD_LINE_1)
    lcd_string(value1data,LCD_LINE_2)

    time.sleep(10)

    # Send some more text
    lcd_string("Uhrzeit:",LCD_LINE_1)
    lcd_string(value2data,LCD_LINE_2)

    time.sleep(10)
    
    # Send some more text
    lcd_string("IPAdresse Octoprint",LCD_LINE_1)
    lcd_string(ipadresse_octoprint,LCD_LINE_2)

    time.sleep(10)

    # Send some more text
    lcd_string("IPAdresse Raspi",LCD_LINE_1)
    lcd_string(ipadresse_raspberry,LCD_LINE_2)

    time.sleep(10)

    # Send some more text
    lcd_string("IPAdresse ESP8266",LCD_LINE_1)
    lcd_string(ipadresse_esp8266,LCD_LINE_2)

    time.sleep(10)





