from Tkinter import *
import RPi.GPIO as GPIO
import time
import sys

carrierWidth = 50
carrierPeriod = 1/float(carrierWidth)

dutyStart = 3
dutyEnd = 12

position1 = 2
position2 = 37

def getDuty(angle):
    duty = float(angle)/180 * (dutyEnd - dutyStart) + dutyStart;
    #print(angle, "deg is", duty)
    return duty;

def rotate(angle):
    pwm.ChangeDutyCycle(getDuty(angle))
    time.sleep(1)

GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)
pwm = GPIO.PWM(18, carrierWidth)

pwm.start(getDuty(position1))
rotate(position1)
rotate(position2)
rotate(position1)
time.sleep(1)
