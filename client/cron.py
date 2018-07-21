import sys
from datetime import datetime, timedelta
from constants import *
import sqlite3
from dateutil import parser

conn = sqlite3.connect(SQLITE_FILE, detect_types=sqlite3.PARSE_DECLTYPES)

conn.execute('''CREATE TABLE IF NOT EXISTS cron
         (NAME           VARCHAR(50)   NOT NULL,
         LASTRUN        DATETIME);''')

time0 = datetime.now().replace(hour=0,minute=0,second=0,microsecond=0,day=1,month=1,year=1970)


# cronstring with format "h x,y,z" means "at X o'clock every x/y/z day of the week"
class Cron:
    cronName = "unknown"
    cronString = ""
    hour = ""
    days = []

    def __init__(self, cronName, cronString):
        self.cronName = cronName
        self.cronString = cronString
        
        parts = self.cronString.split(" ")
        if len(parts) != 2:
            print "Invalid cron string:", self.cronString
            sys.exit(1)

        hour = parts[0].strip()
        days = parts[1].strip()

        if not hour.isdigit():
            print "Hour not valid:", hour
            sys.exit(1)

        self.hour = int(hour)

        if days == "*":
            days = "0,1,2,3,4,5,6"

        days2 = days.split(",")

        self.days = [int(day) for day in days2]

        # make sure there is something in the DB
        try:
            cursor = conn.execute("SELECT * FROM cron WHERE NAME = (?)", (self.cronName,))
            count = 0
            for c in cursor:
                count += 1

            if count == 0:
                conn.execute("INSERT INTO cron (NAME, LASTRUN) VALUES ((?), (?))", (self.cronName, time0,))

        except ValueError as err:
            print("ERR", err)

    def __str__(self):
     return str(self.hour)+"h days:"+','.join([str(x) for x in self.days])

    def nextOccurence(self, now):
        weekStart = now.replace(hour=0,minute=0,second=0,microsecond=0) 
        while weekStart.weekday() != 0:
            weekStart = weekStart - timedelta(days=1)
        # valid week start, now replace with the time (which cannot be *)
        nextOccurence = weekStart.replace(hour=self.hour)

        while nextOccurence<now:
            nextOccurence = nextOccurence + timedelta(days=1)
            while nextOccurence.weekday() not in self.days:
                nextOccurence = nextOccurence + timedelta(days=1)

        return nextOccurence

    def lastDayExecuted(self):
        lastRun = time0
        try:
            cursor = conn.execute("SELECT LASTRUN FROM cron WHERE NAME = (?)", (self.cronName,))
            data=cursor.fetchall()
            lastRun = parser.parse(data[0][0])
        except Error as err:
            pass

        return lastRun

    # we run 5min before the deadline
    # if true, run the action
    def shouldItRun(self, now):
        nextOccurence = self.nextOccurence(now)
        lastRun = self.lastDayExecuted()

        # difference in minutes between now and when it should run
        diff = nextOccurence - now
        diff_minutes = (diff.total_seconds() / 60)
        
        # difference in minutes between last run and when it should run
        diff = nextOccurence - lastRun
        diff_minutes2 = (diff.total_seconds() / 60)

        #print "diff min", diff_minutes
        #print "last Run and next occurence diff", diff, diff_minutes2
        
        if diff_minutes < 5 and diff_minutes2 >= 5:
            cursor.execute("UPDATE cron SET LASTRUN=(?) WHERE NAME=(?)", (nextOccurence, self.cronName,))
            conn.commit()
            return True

        return False