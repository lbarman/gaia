#!/usr/bin/python2
import sys
import requests
import time
import datetime
import subprocess
import urllib
import base64
from os import access, R_OK, W_OK
from os.path import isfile
from constants import *
import RPi.GPIO as GPIO

lastDayFed = None
nextFeedingTime = None

def testRWFile(file):
    if not isfile(file):
        with open(file, 'w') as f:
            f.write("")
    if not access(file, W_OK) or not access(file, R_OK):
        print("Cannot R/W file", file)
        sys.exit(1) 

def getShellOutput(cmd):
    #eg. cmd = ["ps", "-u"]
    o = "NULL"
    try:
        o = subprocess.Popen(cmd,stdout=subprocess.PIPE).communicate()[0];
        o = o.decode('utf-8').strip()
    except:
        pass

    return o

def getDataToUpload(now):

    data = ""
    data += "# feeding\n"
    data += "daily feeding hour: "+str(FEEDING_TIME)+":00:00\n"
    data += "last day fed: "+lastDayFed.strftime("%d.%m.%Y")+"\n"

    feedIn = (now.replace(hour=FEEDING_TIME, minute=0, second=0, microsecond=0) - now)
    if lastDayFed.date() == now.date():
        data += "already fed for today\n\n"
    else:
        data += "NOT yet fed for today\n"
        if feedIn.total_seconds() < 0:
            data += "should feed asap, hang on...\n\n"
        else:
            hms = datetime.timedelta(seconds=int(feedIn.total_seconds()))
            data += "feeding in "+str(hms)+"\n\n"

    data += "# uptime\n"+getShellOutput(["uptime"])+'\n\n'
    data += "# free\n"+getShellOutput(["free"])+'\n\n'
    data += "# df -h\n"+getShellOutput(["df","-h"])+'\n\n'
    #data += "# top\n"+getShellOutput(["top", "-b" "-n1"])+'\n\n'
    
    data = base64.b64encode(bytes(data))
    return data

def contactGaiaWebSite(now):
    params = {
        "ping" : True,
        "token" : GAIA_SECRETTOKEN,
        "local_ts" : now.strftime('%Y-%m-%d %H:%M:%S'),
        "data" : getDataToUpload(now)
    }

    r = requests.get(GAIA_URL, params=params)

def waitingLoop(now):
    contactGaiaWebSite(now)
    print("WaitingLoop: waiting", WAITING_LOOP_SLEEP, "sec")
    time.sleep(WAITING_LOOP_SLEEP)

def buttonPressed():
    print "Button pressed"
    feed(datetime.datetime.now(), "Feeded manually")

def servoAngleToDuty(angle):
    duty = float(angle)/180 * (SERVO_DUTY_END - SERVO_DUTY_START) + SERVO_DUTY_START;
    return duty;

def servoRotate(angle):
    global pwm
    pwm.ChangeDutyCycle(servoAngleToDuty(angle))
    time.sleep(1)

def servoFeed():
    rotate(SERVO_FEED_POS1)
    rotate(SERVO_FEED_POS2)
    rotate(SERVO_FEED_POS1)
    time.sleep(1)

def feed(now, action="Feeded"):
    global lastDayFed
    
    servoFeed()

    lastDayFed = now.date()
    with open(FILE_LAST_DAY_FED, 'w') as f:
        f.write(lastDayFed.strftime("%d.%m.%Y"))

    params = {
        "ping" : True,
        "token" : GAIA_SECRETTOKEN,
        "local_ts" : now.strftime('%Y-%m-%d %H:%M:%S'),
        "data" : base64.b64encode(bytes(action)),
    }

    r = requests.get(GAIA_URL, params=params)

testRWFile(FILE_FEEDING_TIME)
testRWFile(FILE_LAST_DAY_FED)

# parse next feeding time:
with open(FILE_FEEDING_TIME, 'r') as f:
    try:
        lines = f.readlines()
        h = int(lines[0])
        FEEDING_TIME = h
    except:
        pass

# parse last day fed:
with open(FILE_LAST_DAY_FED, 'r') as f:
    try:
        lines = f.readlines()
        d = str(lines[0]).strip()
        t = time.strptime(d, "%d.%m.%Y")
        lastDayFed = datetime.datetime(*t[:6])
    except:
        pass

#set up the GPIOs
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(GPIO_SERVO, GPIO.OUT)
GPIO.setup(GPIO_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)  
GPIO.add_event_detect(GPIO_BUTTON, GPIO.FALLING, callback=buttonPressed, bouncetime=5000)

pwm = GPIO.PWM(GPIO_SERVO, SERVO_CARRIER_WIDTH)
pwm.start(servoAngleToDuty(SERVO_FEED_POS1))

# run
while True:
    now = datetime.datetime.now()

    # do we need to feed Igor? 
    feedIn = (now.replace(hour=FEEDING_TIME, minute=0, second=0, microsecond=0) - now).total_seconds()
    if lastDayFed.date() != now.date() and feedIn < 0:
        feed(now)
    else:
        waitingLoop(now)
