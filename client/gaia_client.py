#!/usr/bin/env python

import requests
import time
import datetime
import subprocess
import urllib
import sys
import base64
from constants import *
from gpio_control import GPIOControl, cleanup_gpios
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

def getDataToUpload(now):
    global igorCron, plantsCron

    data = ""
    data += "# feed igor\n"
    data += "cron: "+str(igorCron)+"\n"
    data += "last day fed: "+str(igorCron.lastDayExecuted())+"\n"
    n = igorCron.nextOccurence(now)
    data += "next occurence: "+str(n)+" (in "+str(n-now)+")\n"
    data += "\n"
    data += "# water plants\n"
    data += "cron: "+str(plantsCron)+"\n"
    data += "last day watered: "+str(plantsCron.lastDayExecuted())+"\n"
    n = plantsCron.nextOccurence(now)
    data += "next occurence: "+str(n)+" (in "+str(n-now)+")\n"
    data += "\n"

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
        "data" : data
    }

    r = requests.get(GAIA_URL, params=params)

    answer = "none, something went wrong"
    if r.status_code != requests.codes.ok:
        print "Gaia not OK! answer", r
    else:
        answer = r.content.strip()
    return answer

def reboot():
    cleanup_gpios()
    command = "/usr/bin/sudo /sbin/shutdown -h now"
    import subprocess
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output = process.communicate()[0]
    print output

def shutdown():
    cleanup_gpios()
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

    # HTTP Request indicating we just fed Igor
    data = base64.b64encode(bytes(action))
    contactGaiaWebSite(now, data)

def water(now):
    global gpio, db
    
    report = gpio.waterPlants()

    # HTTP Request indicating we just watered the plants
    data = base64.b64encode(bytes(report))
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
    now = datetime.datetime.now() #.replace(hour=10,minute=31, second=0)
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
    else:
        print "[gaia-client.py] waiting", WAITING_LOOP_SLEEP, "sec"
        answer = contactGaiaWebSite(now, getDataToUpload(now))

        if answer == "REBOOT":
            contactGaiaWebSite(now, "Gaia requested reboot.")
            reboot()
        if answer == "SHUTDOWN":
            contactGaiaWebSite(now, "Gaia requested shutdown.")
            shutdown()

        time.sleep(WAITING_LOOP_SLEEP)

    print "[gaia-client.py] looping"