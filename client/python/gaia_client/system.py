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

def __getShellOutput(cmd):
    #eg. cmd = ["ps", "-u"]
    o = "NULL"
    try:
        o = subprocess.Popen(cmd,stdout=subprocess.PIPE).communicate()[0];
        o = o.decode('utf-8').strip()
    except:
        pass

    return o

def status():
    res = {}
    res['3. uptime'] = __getShellOutput(["uptime"])
    res['4. free'] = __getShellOutput(["free"])
    res['5. df -h'] = __getShellOutput(["df", "-h"])
    #res['top'] = __getShellOutput(["top", "-b" "-n1"])
    return res

def reboot():
    cleanup_gpios()
    command = "/usr/bin/sudo /sbin/shutdown -r now"
    import subprocess
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output = process.communicate()[0]
    print output

def shutdown():
    cleanup_gpios()
    command = "/usr/bin/sudo /sbin/shutdown -h now"
    import subprocess
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output = process.communicate()[0]
    print output