#!/usr/bin/env python

import requests
import time
import datetime
import urllib
import base64
from constants import *
from gpio_control import GPIOControl, cleanup_gpios
from cron import Cron
import system

gpio = None

def buttonPressed():
    print "Button pressed"
    feed(datetime.datetime.now(), "Feeded manually")

def feed(now, action="Feeded"):
    global gpio, db
    
    gpio.servoFeed()
    contactGaiaWebSite(now, action)

def water(now):
    global gpio, db
    
    report = gpio.waterPlants()
    contactGaiaWebSite(now, report)

def getDataToUpload(now):
    global igorCron, plantsCron

    data = system.status()

    n = igorCron.nextOccurence(now)
    data['1. feed igor'] = [ "cron: "+str(igorCron), 
        "last day fed: "+str(igorCron.lastDayExecuted()),
        "next occurence: "+str(n)+" (in "+str(n-now)+")"]

    n = igorCron.nextOccurence(now)
    data['2. water plants'] = ["cron: "+str(plantsCron),
        "last day fed: "+str(plantsCron.lastDayExecuted()),
        "next occurence: "+str(n)+" (in "+str(n-now)+")"]

    data['3. cron-db'] = igorCron.debug_printDB()


    # encode to str
    s = ""
    for key in data:
        s += "# "+key +'\n'
        for val in data[key]:
            s += val +'\n'
        s += '\n'
    return s

def contactGaiaWebSite(now, data):
    params = {
        "ping" : True,
        "token" : GAIA_SECRETTOKEN,
        "local_ts" : now.strftime('%Y-%m-%d %H:%M:%S'),
        "data" : base64.b64encode(bytes(data.strip()))
    }

    r = requests.get(GAIA_URL, params=params)

    answer = "none, something went wrong"
    if r.status_code != requests.codes.ok:
        print "Gaia not OK! answer", r
    else:
        answer = r.content.strip()
    return answer

print "[gaia-client.py] starting..."

gpio = GPIOControl()
gpio.buttonCallback = buttonPressed

if gpio == None:
    print "GPIO not initialized, quitting"
    sys.exit(1)

print "[gaia-client.py] db and gpio initialized"

igorCron = Cron("igor", IGOR_CRON)
plantsCron = Cron("plants", PLANTS_CRON)

# main loop
sleepCount = 0
while True:
    # toggle Logic LEDS
    gpio.toggleIgorFeedLed()
    gpio.toggleWaterLed()

    now = datetime.datetime.now() 
    print "It is now", now

    print "igor last fed on      : ", igorCron.lastDayExecuted()
    print "feeding in            : ", (igorCron.nextOccurence(now) - now)
    print "plants last watered on: ", plantsCron.lastDayExecuted()
    print "watering in           : ", (plantsCron.nextOccurence(now) - now)

    if igorCron.shouldItRun(now):
        print "feeding igor now"
        feed(now)
    elif plantsCron.shouldItRun(now):
        print "watering plants now"
        water(now)
    elif sleepCount >= GAIA_REPORT_EVERY_X_SLEEP:
        sleepCount = 0

        print "contacting Gaia now"
        answer = contactGaiaWebSite(now, getDataToUpload(now))

        if answer == "REBOOT" or answer == "RESTART":
            contactGaiaWebSite(now, "Gaia requested reboot.")
            system.reboot()
        if answer == "SHUTDOWN":
            contactGaiaWebSite(now, "Gaia requested shutdown.")
            system.shutdown()
        if answer == "FEED":
            contactGaiaWebSite(now, "Gaia requested manual feeding.")
            feed(now)
        if answer == "WATER":
            contactGaiaWebSite(now, "Gaia requested manual plant watering.")
            water(now)

    #print "[gaia-client.py] waiting", WAITING_LOOP_SLEEP, "sec"
    time.sleep(WAITING_LOOP_SLEEP)
    sleepCount += 1