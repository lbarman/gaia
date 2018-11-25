SQLITE_FILE = "sqlite.db"
SQLITE_DATABASE_PATH  = 'db.sqlite'

WAITING_LOOP_SLEEP = 10

GAIA_URL = "gaia_url"
GAIA_SECRETTOKEN = "abc"
GAIA_REPORT_EVERY_X_SLEEP = 60

# GPIOs: button
GPIO_BUTTON = 17
GPIO_BUTTON_DEBOUNCE_TIME = 5000

# GPIOs: feed igor
GPIO_IGOR_LOGIC_LED = 2
GPIO_SERVO = 3
SERVO_CARRIER_WIDTH = 50
SERVO_CARRIER_PERIOD = 1/float(SERVO_CARRIER_WIDTH)

SERVO_DUTY_START = 3
SERVO_DUTY_END = 12

SERVO_FEED_POS1 = 30   # hole is aligned with bottom hole (food is falling)
SERVO_FEED_POS2 = 73   # hole is aligned with reservoir (loading food)
SERVO_WIGGLE_ANGLE = 5 # used to wiggle the hole below the reservoir

# GPIOs: relays
RELAY_GPIO_1 = 19
RELAY_GPIO_2 = 16
RELAY_GPIO_3 = 26
RELAY_GPIO_4 = 20
GPIO_WATER_LOGIC_LED = 21

RELAY_DURATION_FULL_GLASS = float(150) # 150 s to fill a 2dl class

WATER_PLANT_FILL_PIPES_DURATION = 5
WATER_PLANT_RELAY1_DURATION = RELAY_DURATION_FULL_GLASS/2
WATER_PLANT_RELAY2_DURATION = RELAY_DURATION_FULL_GLASS/2
WATER_PLANT_RELAY3_DURATION = RELAY_DURATION_FULL_GLASS
WATER_PLANT_RELAY4_DURATION = RELAY_DURATION_FULL_GLASS # -1 :do not water

# Cron
IGOR_CRON = "12 *"
PLANTS_CRON = "13 1,4"

CRON_REGEX_TESTER = '^(\\d|[01]\\d|2[0-3])h (\\*|([0-6],)*[0-6])$'
DAYS_STRING = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]

from datetime import datetime
CRON_TIME0 = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0, day=1, month=1, year=1970)