#!/usr/bin/env python
import time
import gaia_client.constants as constants
import atexit

try:
    import RPi.GPIO as GPIO
except RuntimeError:
    print("Error importing RPi.GPIO! Is this running with sudo ?")


class ClassWithReport:

    report = ''
    is_verbose = False

    def __init__(self, verbose=False):
        self.is_verbose = verbose

    def new_report(self):
        self.report = ''

    def do_report(self, s):
        self.vprint(s)
        self.report += s + '\n'

    def vprint(self, s):
        if self.verbose:
            print(s)


class GPIOControl(ClassWithReport):
    pwm = None

    feeding_led_state = False
    watering_led_state = False

    def __init__(self, verbose=True):

        super(GPIOControl, self).__init__()

        self.verbose = verbose
        self.report = ''

        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        # turn off the "logic" LEDs
        GPIO.setup(constants.GPIO_IGOR_LOGIC_LED, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(constants.GPIO_WATER_LOGIC_LED, GPIO.OUT, initial=GPIO.LOW)
        GPIO.output(constants.GPIO_IGOR_LOGIC_LED, GPIO.LOW)
        GPIO.output(constants.GPIO_WATER_LOGIC_LED, GPIO.LOW)

        # set up the relays
        GPIO.setup(constants.RELAY_GPIO_1, GPIO.OUT, initial=GPIO.HIGH)
        GPIO.setup(constants.RELAY_GPIO_2, GPIO.OUT, initial=GPIO.HIGH)
        GPIO.setup(constants.RELAY_GPIO_3, GPIO.OUT, initial=GPIO.HIGH)
        GPIO.setup(constants.RELAY_GPIO_4, GPIO.OUT, initial=GPIO.HIGH)

        # redundant, but to be sure
        GPIO.output(constants.RELAY_GPIO_1, GPIO.HIGH)
        GPIO.output(constants.RELAY_GPIO_2, GPIO.HIGH)
        GPIO.output(constants.RELAY_GPIO_3, GPIO.HIGH)
        GPIO.output(constants.RELAY_GPIO_4, GPIO.HIGH)

        # start controlling the servo
        GPIO.setup(constants.GPIO_SERVO, GPIO.OUT)
        self.pwm = GPIO.PWM(constants.GPIO_SERVO, constants.SERVO_CARRIER_WIDTH)
        # startAngle = self.__servoAngleToDuty(SERVO_FEED_POS1)
        # self.pwm.start(startAngle)

    def do_feeding(self):
        self.vprint("Starting feed routine...")

        start_angle = self.__servo_angle_to_duty(constants.SERVO_FEED_POS1)
        self.pwm.start(start_angle)

        self.__servo_rotate(constants.SERVO_FEED_POS1)
        time.sleep(1)

        self.__servo_rotate(constants.SERVO_FEED_POS2)

        i = 0
        while i < 20:
            time.sleep(0.1)
            self.__servo_rotate(constants.SERVO_FEED_POS2 + constants.SERVO_WIGGLE_ANGLE)
            time.sleep(0.1)
            self.__servo_rotate(constants.SERVO_FEED_POS2 - constants.SERVO_WIGGLE_ANGLE)
            i += 1
        time.sleep(0.1)
        self.__servo_rotate(constants.SERVO_FEED_POS2)
        time.sleep(1)

        self.__servo_rotate(constants.SERVO_FEED_POS1)
        time.sleep(1)

        self.pwm.stop()
        self.vprint("Done feeding.")

    def do_watering(self):

        self.new_report()
        self.do_report("Starting plant watering routine...")

        self.__watering_plants_inner_loop(1, constants.RELAY_GPIO_1, constants.WATER_PLANT_RELAY1_DURATION)
        self.__watering_plants_inner_loop(2, constants.RELAY_GPIO_2, constants.WATER_PLANT_RELAY2_DURATION)
        self.__watering_plants_inner_loop(3, constants.RELAY_GPIO_3, constants.WATER_PLANT_RELAY3_DURATION)
        self.__watering_plants_inner_loop(4, constants.RELAY_GPIO_4, constants.WATER_PLANT_RELAY4_DURATION)

        self.do_report("Plant watering routine done.")
        return self.report

    @staticmethod
    def __servo_angle_to_duty(angle):
        duty = float(angle) / 180 * (constants.SERVO_DUTY_END - constants.SERVO_DUTY_START) + constants.SERVO_DUTY_START
        return duty

    def __servo_rotate(self, angle):
        duty = self.__servo_angle_to_duty(angle)
        self.pwm.ChangeDutyCycle(duty)

    def __watering_plants_inner_loop(self, relay_id, gpio_pin, duration_sec):
        if duration_sec == -1:
            self.do_report("Skip watering plant #" + str(relay_id) + ", value -1")
        else:
            t1 = time.time()
            self.do_report("Turning on watering for plant #" + str(relay_id) + ", value " + str(duration_sec))
            GPIO.output(gpio_pin, GPIO.LOW)

            stop = False
            while not stop:
                t2 = time.time()
                if t2 - t1 < duration_sec:
                    time.sleep(1)
                else:
                    stop = True
            GPIO.output(gpio_pin, GPIO.HIGH)
            self.do_report("Turning off watering for plant #" + str(relay_id) + ", after " + str(round(t2 - t1)) +
                           " seconds")
        return self.report

    def fill_watering_tubes(self):
        self.vprint("Filling pipes...")
        self.__watering_plants_inner_loop(1, constants.RELAY_GPIO_1, constants.WATER_PLANT_FILL_PIPES_DURATION)
        self.__watering_plants_inner_loop(2, constants.RELAY_GPIO_2, constants.WATER_PLANT_FILL_PIPES_DURATION)
        self.__watering_plants_inner_loop(3, constants.RELAY_GPIO_3, constants.WATER_PLANT_FILL_PIPES_DURATION)
        self.__watering_plants_inner_loop(4, constants.RELAY_GPIO_4, constants.WATER_PLANT_FILL_PIPES_DURATION)
        self.vprint("Done.")

    def toggle_feeding_led(self):
        if self.feeding_led_state:
            self.feeding_led_state = False
            GPIO.output(constants.GPIO_IGOR_LOGIC_LED, GPIO.LOW)
        else:
            self.feeding_led_state = True
            GPIO.output(constants.GPIO_IGOR_LOGIC_LED, GPIO.HIGH)

    def toggle_watering_led(self):
        if self.watering_led_state:
            self.watering_led_state = False
            GPIO.output(constants.GPIO_WATER_LOGIC_LED, GPIO.LOW)
        else:
            self.watering_led_state = True
            GPIO.output(constants.GPIO_WATER_LOGIC_LED, GPIO.HIGH)


def cleanup_gpios():
    print "Application ending, cleaning up GPIOs"
    GPIO.output(constants.RELAY_GPIO_1, GPIO.HIGH)
    GPIO.output(constants.RELAY_GPIO_2, GPIO.HIGH)
    GPIO.output(constants.RELAY_GPIO_3, GPIO.HIGH)
    GPIO.output(constants.RELAY_GPIO_4, GPIO.HIGH)
    GPIO.output(constants.GPIO_IGOR_LOGIC_LED, GPIO.LOW)
    GPIO.output(constants.GPIO_WATER_LOGIC_LED, GPIO.LOW)
    GPIO.cleanup()


atexit.register(cleanup_gpios)
