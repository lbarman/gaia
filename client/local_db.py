#!/usr/bin/env python

import sys
import time
from os import access, R_OK, W_OK
from os.path import isfile
from constants import *
import datetime

class LocalDatabase:
    lastDayFed = None
    dailyFeedingTime = FEEDING_TIME

    def testRWFile(self, file):
        if not isfile(file):
            with open(file, 'w') as f:
                f.write("")
        if not access(file, W_OK) or not access(file, R_OK):
            print "Cannot R/W file", file
            sys.exit(1) 

    def __init__(self):
        now = datetime.datetime.now()
        self.lastDayFed = now.replace(hour=0,minute=0,second=0,microsecond=0,day=1,month=1,year=1970)
        self.testRWFile(FILE_FEEDING_TIME)
        self.testRWFile(FILE_LAST_DAY_FED)
        self.read()

    def read(self):
        # parse next feeding time:
        with open(FILE_FEEDING_TIME, 'r') as f:
            try:
                lines = f.readlines()
                h = int(lines[-1])
                self.dailyFeedingTime = h
            except:
                pass

        # parse last day fed:
        with open(FILE_LAST_DAY_FED, 'r') as f:
            try:
                lines = f.readlines()
                d = str(lines[0]).strip()
                t = time.strptime(d, "%d.%m.%Y")
                self.lastDayFed = datetime.datetime(*t[:6])
            except:
                pass

    def updateLastDayFed(self):
        self.lastDayFed = datetime.datetime.now().date()
        with open(FILE_LAST_DAY_FED, 'w') as f:
            f.write(self.lastDayFed.strftime("%d.%m.%Y"))