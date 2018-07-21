#!/usr/bin/env python

import requests
import time
import datetime
import subprocess
import urllib
import base64
from constants import *
from gpio_control import GPIOControl
from cron import Cron

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
    global igorCron, plantsCron

    data = ""
    data += "# feed igor\n"
    data += "cron: "+str(igorCron)+"\n"
    data += "last day fed: "+str(igorCron.lastDayExecuted())+"\n"
    n = igorCron.nextOccurence(now)
    data += "next occurence: "+str(n)+" (in "+str(n-now)+")\n"
    data += ""
    data += "# water plants\n"
    data += "cron: "+str(plantsCron)+"\n"
    data += "last day watered: "+str(plantsCron.lastDayExecuted())+"\n"
    n = plantsCron.nextOccurence(now)
    data += "next occurence: "+str(n)+" (in "+str(n-now)+")\n"
    data += ""

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

    if r.status_code == requests.codes.ok:
        print "Gaia not OK! answer", r
    else:
        print "Gaia answer:", r.content

def restart():
    command = "/usr/bin/sudo /sbin/shutdown -r now"
    import subprocess
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output = process.communicate()[0]
    print output

def buttonPressed():
    print "Button pressed"
    feed(datetime.datetime.now(), "Feeded manually")

def feed(now, action="Feeded"):
    global gpio, db
    
    gpio.servoFeed()

    print(action)

    # HTTP Request indicating we just fed Igor
    data = base64.b64encode(bytes(action))
    contactGaiaWebSite(now, data)

def water(now):
    global gpio, db
    
    gpio.waterPlants()

    print(action)

    # HTTP Request indicating we just watered the plants
    data = base64.b64encode(bytes("Plants watered"))
    contactGaiaWebSite(now, data)

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
while True:
    now = datetime.datetime.now()

    print "igor last fed on      : ", igorCron.lastDayExecuted()
    print "feeding in            : ", (igorCron.nextOccurence(now) - now)
    print "plants last watered on: ", plantsCron.lastDayExecuted()
    print "watering in           : ", (plantsCron.nextOccurence(now) - now)

    if igorCron.shouldItRun(now):
        feed(now)
    elif plantsCron.shouldItRun(now):
        water(now)
    else:
        contactGaiaWebSite(now, getDataToUpload(now))
        print "[gaia-client.py] waiting", WAITING_LOOP_SLEEP, "sec"
        time.sleep(WAITING_LOOP_SLEEP)
    print "[gaia-client.py] looping"