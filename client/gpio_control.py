#!/usr/bin/env python
import RPi.GPIO as GPIO
import time
from constants import *
import atexit

class GPIOControl:
    
    pwm = None
    buttonCallback = None

    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        # map the button
        GPIO.setup(GPIO_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)  
        #GPIO.add_event_detect(GPIO_BUTTON, GPIO.FALLING, callback=self.__buttonPressedCallback, bouncetime=GPIO_BUTTON_DEBOUNCE_TIME)

        # set up the relays
        GPIO.setup(RELAY_GPIO_1, GPIO.OUT, initial=GPIO.HIGH)
        GPIO.setup(RELAY_GPIO_2, GPIO.OUT, initial=GPIO.HIGH)
        GPIO.setup(RELAY_GPIO_3, GPIO.OUT, initial=GPIO.HIGH)
        GPIO.setup(RELAY_GPIO_4, GPIO.OUT, initial=GPIO.HIGH)

        # redundant, but to be sure
        GPIO.output(RELAY_GPIO_1, GPIO.HIGH)
        GPIO.output(RELAY_GPIO_2, GPIO.HIGH)
        GPIO.output(RELAY_GPIO_3, GPIO.HIGH)
        GPIO.output(RELAY_GPIO_4, GPIO.HIGH)

        # start controlling the servo
        GPIO.setup(GPIO_SERVO, GPIO.OUT)
        self.pwm = GPIO.PWM(GPIO_SERVO, SERVO_CARRIER_WIDTH)
        #startAngle = self.__servoAngleToDuty(SERVO_FEED_POS1)
        #self.pwm.start(startAngle)

    def __buttonPressedCallback(self, channel):
        if self.buttonCallback == None:
            print "Button pressed, but no callback registered"
        else:
            print "Button pressed, calling callback"
            self.buttonCallback()
        return

    def __servoAngleToDuty(self, angle):
        duty = float(angle)/180 * (SERVO_DUTY_END - SERVO_DUTY_START) + SERVO_DUTY_START;
        return duty;

    def __servoRotate(self, angle):
        duty = self.__servoAngleToDuty(angle)
        self.pwm.ChangeDutyCycle(duty)

    def servoFeed(self):
        print "Starting feed routine..."
        startAngle = self.__servoAngleToDuty(SERVO_FEED_POS1)
        self.pwm.start(startAngle)

        self.__servoRotate(SERVO_FEED_POS1)
        time.sleep(1)

        self.__servoRotate(SERVO_FEED_POS2)

        i = 0
        while i <20:
            time.sleep(0.1)
            self.__servoRotate(SERVO_FEED_POS2+SERVO_WIGGLE_ANGLE)
            time.sleep(0.1)
            self.__servoRotate(SERVO_FEED_POS2-SERVO_WIGGLE_ANGLE)
            i += 1
        time.sleep(0.1)
        self.__servoRotate(SERVO_FEED_POS2)
        time.sleep(1)

        self.__servoRotate(SERVO_FEED_POS1)
        time.sleep(1)

        self.pwm.stop()
        print "Done feeding."

    def __waterPlantInnerLoop(self, relayID, GPIOPin, durationSec):
        report = ""
        if durationSec == -1:
            print "Skip watering plant #" + str(relayID)+", value -1"
            report += "Skip watering plant #" + str(relayID)+", value -1\n"
        else:
            t1 = time.time()
            print "Turning on watering for plant #" + str(relayID)+", value ", durationSec
            report += "Turning on watering for plant #" + str(relayID)+", value "+str(durationSec)+"\n"
            GPIO.output(GPIOPin, GPIO.LOW)

            stop = False
            while not stop:
                t2 = time.time()
                if t2-t1 < durationSec:
                    time.sleep(1)
                else:
                    stop = True
            GPIO.output(GPIOPin, GPIO.HIGH)
            print "Turning off watering for plant #" + str(relayID)+", after", round(t2-t1), "seconds"
            report += "Turning off watering for plant #" + str(relayID)+", after " + str(round(t2-t1)) + " seconds\n"
        return report

    def waterPlants(self):

        report = ""
        print "Starting plant watering routine..."
        report += "Starting plant watering routine...\n"

        report += self.__waterPlantInnerLoop(1, RELAY_GPIO_1, WATER_PLANT_RELAY1_DURATION)
        report += self.__waterPlantInnerLoop(2, RELAY_GPIO_2, WATER_PLANT_RELAY2_DURATION)
        report += self.__waterPlantInnerLoop(3, RELAY_GPIO_3, WATER_PLANT_RELAY3_DURATION)
        report += self.__waterPlantInnerLoop(4, RELAY_GPIO_4, WATER_PLANT_RELAY4_DURATION)

        print "Plant watering routine done."
        report += "Plant watering routine done.\n"

        return report


def cleanup_gpios():
    print "Application ending, cleaning up GPIOs"
    GPIO.output(RELAY_GPIO_1, GPIO.HIGH)
    GPIO.output(RELAY_GPIO_2, GPIO.HIGH)
    GPIO.output(RELAY_GPIO_3, GPIO.HIGH)
    GPIO.output(RELAY_GPIO_4, GPIO.HIGH)
    GPIO.cleanup()

atexit.register(cleanup_gpios)