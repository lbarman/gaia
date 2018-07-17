import RPi.GPIO as GPIO
import time
import sys
from feed_constants import *

def getDuty(angle):
    duty = float(angle)/180 * (dutyEnd - dutyStart) + dutyStart;
    return duty;

def rotate(angle):
    pwm.ChangeDutyCycle(getDuty(angle))
    time.sleep(1)

GPIO.setmode(GPIO.BCM)
GPIO.setup(GPIO_TO_USE, GPIO.OUT)
pwm = GPIO.PWM(GPIO_TO_USE, carrierWidth)

pwm.start(getDuty(position1))
rotate(position1)
rotate(position2)
rotate(position1)
time.sleep(1)
