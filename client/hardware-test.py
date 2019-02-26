#!/usr/bin/python3

import subprocess
import datetime
from os import listdir
from os.path import join

separator = "*" * 60

def shell(cmd):
    result = subprocess.run(cmd, stdout=subprocess.PIPE)
    return result.stdout.decode('utf-8')

# Constants, to be moved somewhere else
LCD_I2C_ADDRESS="0x27"
DHT11_SENSOR_GPIO_PIN = 17
FEEDING_MOTOR_GPIO_PIN = 18
FEEDING_BUTTON_GPIO_PIN = 23

print(separator)
print("*** The DHT11 temperature/humidity ***\n")
import RPi.GPIO as GPIO
import dht11

GPIO.setmode(GPIO.BCM)
instance = dht11.DHT11(pin=DHT11_SENSOR_GPIO_PIN)

result = instance.read()
if result.is_valid():
    print("Temperature: %d C" % result.temperature)
    print("Humidity: %d %%" % result.humidity)
else:
    print("Invalid")

print("Continue ? [Enter]")
input()


print(separator)
print("*** Feeder's continuous servo ***\n")

print("This will start the motor. Press Enter to stop afterwards. Start ? [Enter]")
input()

GPIO.setmode(GPIO.BCM)
GPIO.setup(FEEDING_MOTOR_GPIO_PIN, GPIO.OUT)
p = GPIO.PWM(FEEDING_MOTOR_GPIO_PIN, 2500)
p.start(1)
input('Press return to stop:')   # use raw_input for Python 2
p.stop()


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
print("*** Testing the feeder's button ***\n")


def callback(channel):
    if GPIO.input(FEEDING_BUTTON_GPIO_PIN) == GPIO.HIGH:
        lcd.clear()
        lcd.write_string('BUTTON ___ ' + str(datetime.datetime.now().time())[0:8])
        print("Button pressed  ___")
    else:
        lcd.clear()
        lcd.write_string('BUTTON _-_ ' + str(datetime.datetime.now().time())[0:8])
        print("Button released _-_")


GPIO.setup(FEEDING_BUTTON_GPIO_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.add_event_detect(FEEDING_BUTTON_GPIO_PIN, GPIO.BOTH, callback=callback, bouncetime=200)


print("Continue ? [Enter]")
input()

GPIO.cleanup()