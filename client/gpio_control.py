#!/usr/bin/env python
import RPi.GPIO as GPIO
import time
from constants import *

class GPIOControl:
    
    pwm = None
    buttonCallback = None

    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(GPIO_SERVO, GPIO.OUT)
        GPIO.setup(GPIO_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)  
        GPIO.add_event_detect(GPIO_BUTTON, GPIO.FALLING, callback=self.__buttonPressedCallback, bouncetime=GPIO_BUTTON_DEBOUNCE_TIME)
        self.pwm = GPIO.PWM(GPIO_SERVO, SERVO_CARRIER_WIDTH)

    def __buttonPressedCallback(self, channel):
        if self.buttonCallback == None:
            print "Button pressed, but no callback registered"
        else:
            self.buttonCallback()
        return

    def __servoAngleToDuty(self, angle):
        duty = float(angle)/180 * (SERVO_DUTY_END - SERVO_DUTY_START) + SERVO_DUTY_START;
        return duty;

    def __servoRotate(self, angle):
        duty = self.__servoAngleToDuty(angle)
        self.pwm.ChangeDutyCycle(duty)

    def servoFeed(self):
        startAngle = self.__servoAngleToDuty(SERVO_FEED_POS1)
        self.pwm.start(startAngle)

        self.__servoRotate(SERVO_FEED_POS1)
        time.sleep(1)

        self.__servoRotate(SERVO_FEED_POS2)

        i = 0
        while i <20:
            time.sleep(0.1)
            self.__servoRotate(SERVO_FEED_POS2+10)
            time.sleep(0.1)
            self.__servoRotate(SERVO_FEED_POS2-10)
            i += 1
        self.__servoRotate(SERVO_FEED_POS2)
        time.sleep(1)

        self.__servoRotate(SERVO_FEED_POS1)
        time.sleep(1)

        self.pwm.stop()