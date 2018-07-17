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
GPIO.setwarnings(False)

GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)  

def my_callback(channel):  
        print "falling edge detected on 17" 

GPIO.add_event_detect(17, GPIO.FALLING, callback=my_callback, bouncetime=300)

pwm = GPIO.PWM(GPIO_TO_USE, carrierWidth)

pwm.start(getDuty(position1Degree))
rotate(position1Degree)
rotate(position2Degree)
rotate(position1Degree)
time.sleep(1)


try:  
    while True:
        print "Sleeping"
        time.sleep(1)
except KeyboardInterrupt:  
    GPIO.cleanup()       # clean up GPIO on CTRL+C exit  
GPIO.cleanup()
