#!/usr/bin/env python3
import sys
import requests
import time
import datetime
import subprocess
import urllib
import base64

FEEDING_TIME = 17  # 5pm daily
WAITING_LOOP_SLEEP = 1
GAIA_URL = "https://gaia.lbarman.ch/index.php"
GAIA_SECRETTOKEN = "nSWXz8p7BsdY74NGNQVqJr4e"

nextFeedingTime = None

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
    feedIn = (now.replace(hour=FEEDING_TIME, minute=0, second=0, microsecond=0) - now)
    if feedIn.total_seconds() < 0:
        data += "already fed for today\n\n"
    else:
        hms = datetime.timedelta(seconds=int(feedIn.total_seconds()))
        data += "feeding in "+str(hms)+"\n\n"

    data += "# uptime\n"+getShellOutput(["uptime"])+'\n\n'
    data += "# free\n"+getShellOutput(["free"])+'\n\n'
    data += "# df -h\n"+getShellOutput(["df","-h"])+'\n\n'
    #data += "# top\n"+getShellOutput(["top", "-b" "-n1"])+'\n\n'
    
    data = base64.b64encode(bytes(data, "utf-8"))
    return data

def contactGaiaWebSite():
    now = datetime.datetime.now()
    params = {
        "ping" : True,
        "token" : GAIA_SECRETTOKEN,
        "local_ts" : now.strftime('%Y-%m-%d %H:%M:%S'),
        "data" : getDataToUpload(now)
    }

    r = requests.get(GAIA_URL, params=params)
    print(r.text)

    sys.exit(1)

def waitingLoop():
    contactGaiaWebSite()
    print("WaitingLoop: waiting", WAITING_LOOP_SLEEP, "sec")
    time.sleep(WAITING_LOOP_SLEEP)


# run
while True:
    waitingLoop()