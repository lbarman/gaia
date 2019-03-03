#!/usr/bin/python3
import sys
import os.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

import subprocess
import datetime
from os import listdir
from os.path import join
import gaia_client.gpio_init as gpios
import gaia_client.dht11 as dht11
import gaia_client.constants as constants
from RPLCD.i2c import CharLCD

try:
    import RPi.GPIO as GPIO
except RuntimeError:
    print("Error importing RPi.GPIO! Is this running with sudo ?")
    sys.exit(1)

separator = "*" * 60

def shell(cmd):
    result = subprocess.run(cmd, stdout=subprocess.PIPE)
    return result.stdout.decode('utf-8')

print(separator)
print("*** The DHT11 temperature/humidity ***\n")

instance = dht11.DHT11(pin=gpios.GPIO_PIN_DHT11)

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
print("Pin is expected to be", gpios.LCD_I2C_ADDRESS, ". If not, edit the constants. Continue ? [Enter]")
input()

lcd = CharLCD('PCF8574', int(gpios.LCD_I2C_ADDRESS, 16))
lcd.clear()
lcd.write_string('LCD OK ' + str(datetime.datetime.now().time())[0:8])

print("LCD should read \"OK\". Continue ? [Enter]")
input()

print(separator)
print("*** Testing for the W-1 sensors ***\n")

w1sensors = [f for f in listdir(constants.ONE_WIRE_DEVICES_PATH) if f.startswith(constants.ONE_WIRE_SENSOR_NAME_STARTSWITH)]
print("There should be two sensors shown:")
print(",".join(w1sensors) + "\n")

for w1sensor in w1sensors:
    print("Reading from", w1sensor)
    with open(join(constants.ONE_WIRE_DEVICES_PATH, w1sensor, constants.ONE_WIRE_SENSOR_DATA_LOCATION) , 'r') as content_file:
        print(content_file.read())


print("Continue ? [Enter]")
input()

print(separator)
print("*** Testing the feeder's led ***\n")

GPIO.output(gpios.GPIO_PIN_LED_FEEDING, GPIO.HIGH)
print("Feeder's LED should be ON. Continue ? [Enter]")
input()

GPIO.output(gpios.GPIO_PIN_LED_FEEDING, GPIO.LOW)
print("Feeder's LED should be OFF. Continue ? [Enter]")
input()

print(separator)
print("*** Testing the feeder's button ***\n")
print("Press on the button. The LCD should display the event.")

def callback(channel):
    if GPIO.input(gpios.GPIO_PIN_BUTTON_FEEDING) == GPIO.HIGH:
        lcd.clear()
        lcd.write_string('BUTTON1 ___ ' + str(datetime.datetime.now().time())[0:8])
        print("Feeder's Button pressed  ___")
    else:
        lcd.clear()
        lcd.write_string('BUTTON1 _-_ ' + str(datetime.datetime.now().time())[0:8])
        print("Feeder's Button released _-_")


GPIO.setup(gpios.GPIO_PIN_BUTTON_FEEDING, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.add_event_detect(gpios.GPIO_PIN_BUTTON_FEEDING, GPIO.BOTH, callback=callback, bouncetime=200)

print("Continue ? [Enter]")
input()

print(separator)
print("*** Feeder's continuous servo ***\n")

print("This will start the motor. Press Enter to stop afterwards. Start ? [Enter]")
input()

GPIO.setup(gpios.GPIO_PIN_SERVO_FEEDING, GPIO.OUT)
p = GPIO.PWM(gpios.GPIO_PIN_SERVO_FEEDING, 2500)
p.start(1)
input('Press return to stop:')   # use raw_input for Python 2
p.stop()

print(separator)
print("*** Testing the watering system's led ***\n")

GPIO.output(gpios.GPIO_PIN_LED_WATERING, GPIO.HIGH)
print("Watering system's LED should be ON. Continue ? [Enter]")
input()

GPIO.output(gpios.GPIO_PIN_LED_WATERING, GPIO.LOW)
print("Watering system's LED should be OFF. Continue ? [Enter]")
input()

print(separator)
print("*** Testing the watering systems's button ***\n")
print("Press on the button. The LCD should display the event.")

def callback2(channel):
    if GPIO.input(gpios.GPIO_PIN_BUTTON_WATERING) == GPIO.HIGH:
        lcd.clear()
        lcd.write_string('BUTTON2 ___ ' + str(datetime.datetime.now().time())[0:8])
        print("Watering System's Button pressed  ___")
    else:
        lcd.clear()
        lcd.write_string('BUTTON2 _-_ ' + str(datetime.datetime.now().time())[0:8])
        print("Watering System's Button released _-_")


GPIO.setup(gpios.GPIO_PIN_BUTTON_WATERING, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.add_event_detect(gpios.GPIO_PIN_BUTTON_WATERING, GPIO.BOTH, callback=callback2, bouncetime=200)

print("Continue ? [Enter]")
input()

print(separator)
print("*** Testing the watering system's led ***\n")

def test_relay(id, pin):
    GPIO.output(pin, GPIO.HIGH)
    print("Watering system's Relay", id, "should be ON. Continue ? [Enter]")
    input()

    GPIO.output(pin, GPIO.LOW)
    print("Watering system's Relay", id, "should be OFF. Continue ? [Enter]")
    input()

test_relay(1, gpios.GPIO_PIN_RELAY1_WATERING)
test_relay(2, gpios.GPIO_PIN_RELAY2_WATERING)
test_relay(3, gpios.GPIO_PIN_RELAY3_WATERING)
test_relay(4, gpios.GPIO_PIN_RELAY4_WATERING)

print("All done, GPIO's should cleanup automatically.")