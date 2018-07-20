#!/usr/bin/env python

import requests
import time
import datetime
import subprocess
import urllib
import base64
from constants import *
from gpio_control import GPIOControl
from local_db import LocalDatabase

db = None
gpio = None

def getShellOutput(cmd):
    #eg. cmd = ["ps", "-u"]
    o = "NULL"
    try:
        o = subprocess.Popen(cmd,stdout=subprocess.PIPE).communicate()[0];
        o = o.decode('utf-8').strip()
    except:
        pass

    return o

def sameDay(date1, date2):
    if date1.replace(hour=0,minute=0,second=0,microsecond=0) == date2.replace(hour=0,minute=0,second=0,microsecond=0):
        return True
    return False

def getDataToUpload(now):
    global db

    data = ""
    data += "# feeding\n"
    data += "daily feeding hour: "+str(db.dailyFeedingTime)+":00:00\n"
    data += "last day fed: "+db.lastDayFed.strftime("%d.%m.%Y")+"\n"

    feedIn = (now.replace(hour=db.dailyFeedingTime, minute=0, second=0, microsecond=0) - now)
    if sameDay(db.lastDayFed,now):
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

def contactGaiaWebSite(now, data):
    params = {
        "ping" : True,
        "token" : GAIA_SECRETTOKEN,
        "local_ts" : now.strftime('%Y-%m-%d %H:%M:%S'),
        "data" : getDataToUpload(now)
    }

    r = requests.get(GAIA_URL, params=params)

def buttonPressed():
    print "Button pressed"
    feed(datetime.datetime.now(), "Feeded manually")

def feed(now, action="Feeded"):
    global gpio, db
    
    gpio.servoFeed()
    db.updateLastDayFed()

    print(action)

    # HTTP Request indicating we just fed Igor
    data = base64.b64encode(bytes(action))
    contactGaiaWebSite(now, data)

print "[gaia-client.py] starting..."

db = LocalDatabase()
gpio = GPIOControl()
gpio.buttonCallback = buttonPressed

if db == None:
    print "DB not initialized, quitting"
    sys.exit(1)

if gpio == None:
    print "GPIO not initialized, quitting"
    sys.exit(1)

print "[gaia-client.py] db and gpio initialized"

# main loop
while True:
    now = datetime.datetime.now()

    print "last fed on", db.lastDayFed

    # do we need to feed Igor? 
    feedIn = (now.replace(hour=db.dailyFeedingTime, minute=0, second=0, microsecond=0) - now).total_seconds()
    
    if sameDay(db.lastDayFed,now) and feedIn < 0:
        feed(now)
    else:
        contactGaiaWebSite(now, getDataToUpload(now))
        print "[gaia-client.py] waiting", WAITING_LOOP_SLEEP, "sec"
        time.sleep(WAITING_LOOP_SLEEP)
    print "[gaia-client.py] looping"