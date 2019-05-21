#!/usr/bin/env python
import sys
import time
import gaia_client.constants as constants
import gaia_client.gpio_init as gpios
from os import listdir
from os.path import join
from RPLCD.i2c import CharLCD
import threading
from datetime import datetime
from gaia_client.DHT22 import DHT22Sensor

try:
    import RPi.GPIO as GPIO
except RuntimeError:
    print("Error importing RPi.GPIO! Is this running with sudo ?")
    sys.exit(1)

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

    feeding_led_state = False
    watering_led_state = False
    lcd = None
    pwm = None
    last_sensor_report = dict()
    lock = None
    dht22sensor = None

    def __init__(self, verbose=True):

        super().__init__()

        self.verbose = verbose
        self.report = ''
        self.last_sensor_report = dict()
        self.last_sensor_report['t1'] = -1
        self.last_sensor_report['humidity'] = -1
        self.last_sensor_report['t2'] = -1
        self.last_sensor_report['t3'] = -1
        self.lock = threading.Lock()

        # create DHT22 sensor
        self.dht22sensor = DHT22Sensor(gpio=gpios.GPIO_PIN_AM2301)

        # instantiate LCD screen
        self.lcd = CharLCD(gpios.LCD_TYPE, int(gpios.LCD_I2C_ADDRESS, 16), charmap='A00')
        self.lcd.clear()

        # add hooks for buttons
        GPIO.setup(gpios.GPIO_PIN_BUTTON_FEEDING, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(gpios.GPIO_PIN_BUTTON_WATERING, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

        GPIO.add_event_detect(gpios.GPIO_PIN_BUTTON_FEEDING, GPIO.BOTH, callback=self.__button_feeding_pressed, bouncetime=gpios.BUTTON_DEBOUNCE_DURATION)
        GPIO.add_event_detect(gpios.GPIO_PIN_BUTTON_WATERING, GPIO.BOTH, callback=self.__button_watering_pressed, bouncetime=gpios.BUTTON_DEBOUNCE_DURATION)

    def __button_feeding_pressed(self, channel=None):
        if not self.lock(blocking=False):
            self.lcd_write('Busy, cancelling.')
            return
        else:
            if GPIO.input(gpios.GPIO_PIN_BUTTON_FEEDING) == GPIO.HIGH:
                self.lcd_write('Turning on Feeder')

                # instantiate motor's PWM
                self.pwm = GPIO.PWM(gpios.GPIO_PIN_SERVO_FEEDING, gpios.SERVO_ACTIVE_PWM)
                self.pwm.start(1)
            else:
                self.lcd_write('Turning off Feeder')
                self.pwm.stop(1)

            self.lock.release()

    def __button_watering_pressed(self, channel=None):
        if not self.lock(blocking=False):
            self.lcd_write('Busy, cancelling.')
            return
        else:
            if GPIO.input(gpios.GPIO_PIN_BUTTON_FEEDING) == GPIO.HIGH:
                self.lcd_write('Turning on Watering')
                GPIO.output(gpios.GPIO_PIN_RELAY1_WATERING, GPIO.LOW)
                GPIO.output(gpios.GPIO_PIN_RELAY2_WATERING, GPIO.LOW)
                GPIO.output(gpios.GPIO_PIN_RELAY3_WATERING, GPIO.LOW)
                GPIO.output(gpios.GPIO_PIN_RELAY4_WATERING, GPIO.LOW)
            else:
                self.lcd_write('Turning off Watering')
                GPIO.output(gpios.GPIO_PIN_RELAY1_WATERING, GPIO.HIGH)
                GPIO.output(gpios.GPIO_PIN_RELAY2_WATERING, GPIO.HIGH)
                GPIO.output(gpios.GPIO_PIN_RELAY3_WATERING, GPIO.HIGH)
                GPIO.output(gpios.GPIO_PIN_RELAY4_WATERING, GPIO.HIGH)

            self.lock.release()

    def lcd_write(self, text):
        self.lcd.clear()
        self.lcd.write_string(text)

    def lcd_clear(self):
        self.lcd.clear()

    def do_feeding(self):
        with self.lock:
            self.lcd_write("Feeding...")
            self.new_report()
            self.do_report("Starting feed routine...")

            t1 = time.time()


            # instantiate motor's PWM
            self.pwm = GPIO.PWM(gpios.GPIO_PIN_SERVO_FEEDING, gpios.SERVO_ACTIVE_PWM)

            self.pwm.start(1)

            i = 1
            stop = False
            while not stop:
                t2 = time.time()
                self.lcd_write("Feeding" + "."*i)
                i = (i + 1)%3
                if t2 - t1 < constants.FISH_SERVO_ACTIVE_DURATION:
                    time.sleep(0.1)
                else:
                    stop = True

            self.pwm.stop(1)

            self.do_report("Stopping feeding after " + str(round(t2 - t1)) + " seconds")

        self.lcd_write("OK.")
        return self.report

    def do_watering(self):
        with self.lock:
            self.lcd_write("Watering...")
            self.new_report()
            self.do_report("Starting plant watering routine...")

            self.__watering_plants_inner_loop(1, gpios.GPIO_PIN_RELAY1_WATERING, constants.WATER_PLANT_RELAY1_DURATION)
            self.__watering_plants_inner_loop(2, gpios.GPIO_PIN_RELAY2_WATERING, constants.WATER_PLANT_RELAY2_DURATION)
            self.__watering_plants_inner_loop(3, gpios.GPIO_PIN_RELAY3_WATERING, constants.WATER_PLANT_RELAY3_DURATION)
            self.__watering_plants_inner_loop(4, gpios.GPIO_PIN_RELAY4_WATERING, constants.WATER_PLANT_RELAY4_DURATION)

            self.do_report("Plant watering routine done.")

        self.lcd_write("OK.")
        return self.report


    def __watering_plants_inner_loop(self, relay_id, gpio_pin, duration_sec):
        if duration_sec == -1:
            self.do_report("Skip watering plant #" + str(relay_id) + ", value -1")
        else:
            t1 = time.time()
            self.do_report("Turning on watering for plant #" + str(relay_id) + ", value " + str(duration_sec))
            GPIO.output(gpio_pin, GPIO.LOW)

            i = 1
            stop = False
            while not stop:
                t2 = time.time()
                self.lcd_write("Watering " + str(relay_id) + "."*i)
                i = (i + 1)%3
                if t2 - t1 < duration_sec:
                    time.sleep(1)
                else:
                    stop = True
            GPIO.output(gpio_pin, GPIO.HIGH)
            self.do_report("Turning off watering for plant #" + str(relay_id) + ", after " + str(round(t2 - t1)) +
                           " seconds")
        return self.report

    def fill_watering_tubes(self):
        with self.lock:
            self.lcd_write("Filling pipes...")
            self.vprint("Filling pipes...")
            self.__watering_plants_inner_loop(1, gpios.GPIO_PIN_RELAY1_WATERING, constants.WATER_PLANT_FILL_PIPES_DURATION)
            self.__watering_plants_inner_loop(2, gpios.GPIO_PIN_RELAY2_WATERING, constants.WATER_PLANT_FILL_PIPES_DURATION)
            self.__watering_plants_inner_loop(3, gpios.GPIO_PIN_RELAY3_WATERING, constants.WATER_PLANT_FILL_PIPES_DURATION)
            self.__watering_plants_inner_loop(4, gpios.GPIO_PIN_RELAY4_WATERING, constants.WATER_PLANT_FILL_PIPES_DURATION)
            self.vprint("Done.")
        self.lcd_write("OK.")

    def toggle_feeding_led(self):
        if self.feeding_led_state:
            self.feeding_led_state = False
            GPIO.output(gpios.GPIO_PIN_LED_FEEDING, GPIO.LOW)
        else:
            self.feeding_led_state = True
            GPIO.output(gpios.GPIO_PIN_LED_FEEDING, GPIO.HIGH)

    def toggle_watering_led(self):
        if self.watering_led_state:
            self.watering_led_state = False
            GPIO.output(gpios.GPIO_PIN_LED_WATERING, GPIO.LOW)
        else:
            self.watering_led_state = True
            GPIO.output(gpios.GPIO_PIN_LED_WATERING, GPIO.HIGH)

    def read_temperature_sensors(self):
        res = dict()
        res['t1'] = -1
        res['humidity'] = -1
        res['t2'] = -1
        res['t3'] = -1

        # read DHT11 sensor
        t1, humidity, staleness, = self.dht22sensor.read()
        res['t1'] = t1
        res['humidity'] = humidity

        w1sensors = [f for f in listdir(constants.ONE_WIRE_DEVICES_PATH) if
                     f.startswith(constants.ONE_WIRE_SENSOR_NAME_STARTSWITH)]

        # read from the 1-Wire sensors
        i = 2
        for w1sensor in w1sensors:
            try:
                with open(join(constants.ONE_WIRE_DEVICES_PATH, w1sensor, constants.ONE_WIRE_SENSOR_DATA_LOCATION),
                      'r') as content_file:
                    text = content_file.read()
                    if "YES" in text:
                        value = text[text.find("t=")+2:].strip()
                        temp = float(value) / 1000
                        res['t'+str(i)] = temp
                        i += 1
            except:
                pass


        self.last_sensor_report['t1'] = res['t1']
        self.last_sensor_report['humidity'] = res['humidity']
        self.last_sensor_report['t2'] = res['t2']
        self.last_sensor_report['t3'] = res['t3']

        return res

    def lcd_print_status(self):
        time = str(datetime.now().time())[0:5]
        sensors = str(round(self.last_sensor_report['t1']))+"° "+str(round(self.last_sensor_report['humidity']))+"% " + str(round(self.last_sensor_report['t2']))+"° " + str(round(self.last_sensor_report['t3']))+"°"
        #sensors = str(round(self.last_sensor_report['t2'], 1))+"° " + str(round(self.last_sensor_report['t3'], 1))+"°"

        self.lcd_write("Gaia " + time + '\r\n' + sensors)

