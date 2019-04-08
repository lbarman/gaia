# Control loop & Gaia Server
WAITING_LOOP_SLEEP = 10

GAIA_GRPC_URL = "gaiagrpc.lbarman.ch"
GAIA_GRPC_USE_SSL = True
GAIA_SECRETTOKEN = "abc"
GAIA_REPORT_EVERY_X_SLEEP = 60

# Database
SQLITE_FILE = "sqlite.db"
SQLITE_DATABASE_PATH  = 'db.sqlite'

# Cron
CRON_REGEX_TESTER = '^(\\d|[01]\\d|2[0-3])h (\\*|([0-6],)*[0-6])$'
DAYS_STRING = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]

from datetime import datetime
CRON_TIME0 = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0, day=1, month=1, year=1970)

# Path for reading the 1-Wire devices
ONE_WIRE_DEVICES_PATH = "/sys/bus/w1/devices/"
ONE_WIRE_SENSOR_NAME_STARTSWITH = "28-"
ONE_WIRE_SENSOR_DATA_LOCATION = "w1_slave"

# Feeding & Watering's config; this can be overridden with whatever's in the database
FEEDING_DEFAULT_ENABLED = True
FEEDING_DEFAULT_CRONSTRING = "12h 0,2,4,6"
WATERING_DEFAULT_ENABLED = True
WATERING_DEFAULT_CRONSTRING = "13h 1,4"

FISH_SERVO_ACTIVE_DURATION=12.5 #in seconds
RELAY_DURATION_FULL_GLASS = float(150) # 150 s to fill a 2dl class

WATER_PLANT_FILL_PIPES_DURATION = 5
WATER_PLANT_RELAY1_DURATION = RELAY_DURATION_FULL_GLASS/2
WATER_PLANT_RELAY2_DURATION = RELAY_DURATION_FULL_GLASS/2
WATER_PLANT_RELAY3_DURATION = RELAY_DURATION_FULL_GLASS
WATER_PLANT_RELAY4_DURATION = RELAY_DURATION_FULL_GLASS # -1 :do not water