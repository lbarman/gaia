#!/usr/bin/python3

import subprocess
import datetime
from os import listdir
from os.path import join
import RPi.GPIO as GPIO

separator = "*" * 60

def shell(cmd):
    result = subprocess.run(cmd, stdout=subprocess.PIPE)
    return result.stdout.decode('utf-8')

from constants_hardware import *

LCD_I2C_ADDRESS="0x27"

print(separator)
print("*** The DHT11 temperature/humidity ***\n")
import dht11

instance = dht11.DHT11(pin=GPIO_PIN_DHT11)

result = instance.read()
if result.is_valid():
    print("Temperature: %d C" % result.temperature)
    print("Humidity: %d %%" % result.humidity)
else:
    print("Invalid")

print("Continue ? [Enter]")
input()

print(separator)
print("*** Testing for the LCD screen ***\n")
print("i2cdetect -y 1 should show exactly one address")
print(shell(['i2cdetect', '-y', '1']))
print("Pin is expected to be", LCD_I2C_ADDRESS, ". If not, edit the constants. Continue ? [Enter]")
input()

from RPLCD.i2c import CharLCD
lcd = CharLCD('PCF8574', int(LCD_I2C_ADDRESS, 16))
lcd.clear()
lcd.write_string('LCD OK ' + str(datetime.datetime.now().time())[0:8])

print("LCD should read \"OK\". Continue ? [Enter]")
input()

print(separator)
print("*** Testing for the W-1 sensors ***\n")
w1devices = "/sys/bus/w1/devices/"
w1sensors = [f for f in listdir(w1devices) if f.startswith("28-")]
print("There should be two sensors shown:")
print(",".join(w1sensors) + "\n")

for w1sensor in w1sensors:
    print("Reading from", w1sensor)
    with open(join(w1devices, w1sensor, "w1_slave") , 'r') as content_file:
        print(content_file.read())


print("Continue ? [Enter]")
input()

print(separator)
print("*** Testing the feeder's led ***\n")

GPIO.output(GPIO_PIN_LED_FEEDING, GPIO.HIGH)
print("Feeder's LED should be ON. Continue ? [Enter]")
input()

GPIO.output(GPIO_PIN_LED_FEEDING, GPIO.LOW)
print("Feeder's LED should be OFF. Continue ? [Enter]")
input()

print(separator)
print("*** Testing the feeder's button ***\n")
print("Press on the button. The LCD should display the event.")

def callback(channel):
    if GPIO.input(GPIO_PIN_BUTTON_FEEDING) == GPIO.HIGH:
        lcd.clear()
        lcd.write_string('BUTTON1 ___ ' + str(datetime.datetime.now().time())[0:8])
        print("Feeder's Button pressed  ___")
    else:
        lcd.clear()
        lcd.write_string('BUTTON1 _-_ ' + str(datetime.datetime.now().time())[0:8])
        print("Feeder's Button released _-_")


GPIO.setup(GPIO_PIN_BUTTON_FEEDING, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.add_event_detect(GPIO_PIN_BUTTON_FEEDING, GPIO.BOTH, callback=callback, bouncetime=200)

print("Continue ? [Enter]")
input()

print(separator)
print("*** Feeder's continuous servo ***\n")

print("This will start the motor. Press Enter to stop afterwards. Start ? [Enter]")
input()

GPIO.setup(GPIO_PIN_SERVO_FEEDING, GPIO.OUT)
p = GPIO.PWM(GPIO_PIN_SERVO_FEEDING, 2500)
p.start(1)
input('Press return to stop:')   # use raw_input for Python 2
p.stop()

print(separator)
print("*** Testing the watering system's led ***\n")

GPIO.output(GPIO_PIN_LED_WATERING, GPIO.HIGH)
print("Watering system's LED should be ON. Continue ? [Enter]")
input()

GPIO.output(GPIO_PIN_LED_WATERING, GPIO.LOW)
print("Watering system's LED should be OFF. Continue ? [Enter]")
input()

print(separator)
print("*** Testing the watering systems's button ***\n")
print("Press on the button. The LCD should display the event.")

def callback2(channel):
    if GPIO.input(GPIO_PIN_BUTTON_WATERING) == GPIO.HIGH:
        lcd.clear()
        lcd.write_string('BUTTON2 ___ ' + str(datetime.datetime.now().time())[0:8])
        print("Watering System's Button pressed  ___")
    else:
        lcd.clear()
        lcd.write_string('BUTTON2 _-_ ' + str(datetime.datetime.now().time())[0:8])
        print("Watering System's Button released _-_")


GPIO.setup(GPIO_PIN_BUTTON_WATERING, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.add_event_detect(GPIO_PIN_BUTTON_WATERING, GPIO.BOTH, callback=callback2, bouncetime=200)

print("Continue ? [Enter]")
input()

print(separator)
print("*** Testing the watering system's led ***\n")

GPIO.output(GPIO_PIN_RELAY1_WATERING, GPIO.HIGH)
print("Watering system's Relay 1 should be ON. Continue ? [Enter]")
input()

GPIO.output(GPIO_PIN_RELAY1_WATERING, GPIO.LOW)
print("Watering system's Relay 1 should be OFF. Continue ? [Enter]")
input()

GPIO.output(GPIO_PIN_RELAY2_WATERING, GPIO.HIGH)
print("Watering system's Relay 2 should be ON. Continue ? [Enter]")
input()

GPIO.output(GPIO_PIN_RELAY2_WATERING, GPIO.LOW)
print("Watering system's Relay 2 should be OFF. Continue ? [Enter]")
input()

GPIO.output(GPIO_PIN_RELAY3_WATERING, GPIO.HIGH)
print("Watering system's Relay 3 should be ON. Continue ? [Enter]")
input()

GPIO.output(GPIO_PIN_RELAY3_WATERING, GPIO.LOW)
print("Watering system's Relay 3 should be OFF. Continue ? [Enter]")
input()

GPIO.output(GPIO_PIN_RELAY4_WATERING, GPIO.HIGH)
print("Watering system's Relay 4 should be ON. Continue ? [Enter]")
input()

GPIO.output(GPIO_PIN_RELAY4_WATERING, GPIO.LOW)
print("Watering system's Relay 4 should be OFF. Continue ? [Enter]")
input()

print("All done, cleaning up the GPIO's.")
GPIO.cleanup()