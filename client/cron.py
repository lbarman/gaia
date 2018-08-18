from datetime import datetime, timedelta
from constants import *
import sqlite3
from dateutil import parser

# a Cron task runs exactly once in [target-CRON_WINDOW_BEFORE_DEADLINE; target] if called during that time
CRON_WINDOW_BEFORE_DEADLINE = 30

# this is instantiated by the Cron task
conn = None

# cronstring with format "h x,y,z" means "at X o'clock every x/y/z day of the week"
class Cron:
    time0 = datetime.now().replace(hour=0,minute=0,second=0,microsecond=0,day=1,month=1,year=1970)
    cronName = "unknown"
    cronString = ""
    hour = ""
    days = []
    daysStrings = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]

    def __init__(self, cronName, cronString, sqliteMemoryMode=False):
        global conn

        # first, establish the connection to the SQLITE database if not already done
        # this also allows for testing if memory=True
        if conn == None:
            if sqliteMemoryMode:
                print "[warning] Instantiating the cron DB only in memory"
                conn = sqlite3.connect(":memory:", detect_types=sqlite3.PARSE_DECLTYPES)
            else:
                conn = sqlite3.connect(SQLITE_FILE, detect_types=sqlite3.PARSE_DECLTYPES)

        conn.execute('''CREATE TABLE IF NOT EXISTS cron
                 (NAME           VARCHAR(50)   NOT NULL,
                 LASTRUN        DATETIME);''')

        # then, create this Cron. Parse the data and standardize it
        self.cronName = cronName
        self.cronString = cronString
        
        parts = self.cronString.split(" ")
        if len(parts) != 2:
            raise ValueError("Invalid cron string:" + self.cronString)

        hour = parts[0].strip()
        days = parts[1].strip()

        if not hour.isdigit():
            raise ValueError("Hour not valid:" + hour)

        self.hour = int(hour)

        if days == "*":
            days = "0,1,2,3,4,5,6"

        days2 = days.split(",")

        self.days = [int(day) for day in days2]
        self.days = sorted(self.days)

        for day in self.days:
            if day < 0 or day > 6:
                raise ValueError("Day not valid:" + str(day))

        # make sure there is something in the DB w.r.t to this cron
        try:
            cursor = conn.execute("SELECT * FROM cron WHERE NAME = (?)", (self.cronName,))
            count = 0
            for c in cursor:
                count += 1

            if count == 0:
                conn.execute("INSERT INTO cron (NAME, LASTRUN) VALUES ((?), (?))", (self.cronName, self.time0,))

        except ValueError as err:
            print("Cron error:", err)

    def __str__(self):
        return str(self.hour)+"h on "+','.join([self.daysStrings[x] for x in self.days])

    def nextOccurence(self, now):
        nextOccurence = self.__nextOccurenceIrrespectiveToLastRun(now)
        lastRun = self.lastDayExecuted()

        if nextOccurence == lastRun:
            return self.__nextOccurenceIrrespectiveToLastRun(lastRun)

        return nextOccurence

    def __nextOccurenceIrrespectiveToLastRun(self, now):
        weekStart = now.replace(hour=0,minute=0,second=0,microsecond=0) 
        while weekStart.weekday() != 0:
            weekStart = weekStart - timedelta(days=1)
        # valid week start, now replace with the time (which cannot be *)
        nextOccurence = weekStart.replace(hour=self.hour)

        while nextOccurence<=now:
            nextOccurence = nextOccurence + timedelta(days=1)
            while nextOccurence.weekday() not in self.days:
                nextOccurence = nextOccurence + timedelta(days=1)

        return nextOccurence

    def lastDayExecuted(self):
        global conn
        lastRun = self.time0
        try:
            cursor = conn.execute("SELECT LASTRUN FROM cron WHERE NAME = (?)", (self.cronName,))
            data=cursor.fetchall()
            lastRun = parser.parse(data[0][0])
        except Error as err:
            pass

        return lastRun

    # we run 30min before the deadline
    # if true, run the action
    # Statemachine:
    #    IF: next target is closer than CRON_WINDOW_BEFORE_DEADLINE
    #       IF: last_run is not within [next target - CRON_WINDOW_BEFORE_DEADLINE; now]
    #           run, set last_run to target
    #       ELSE: do nothing
    #    ELSE: do nothing
    def shouldItRun(self, now):
        global conn, CRON_WINDOW_BEFORE_DEADLINE
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
        
        # if: next execution is soon, CHECK: last execution must be a long time ago
        if diff_minutes < CRON_WINDOW_BEFORE_DEADLINE and diff_minutes2 >= CRON_WINDOW_BEFORE_DEADLINE:
            conn.execute("UPDATE cron SET LASTRUN=(?) WHERE NAME=(?)", (nextOccurence, self.cronName,))
            conn.commit()
            return True

        return False

    def debug_truncateDB(self):
        global conn
        conn.execute("DROP TABLE cron;")
        conn.execute('''CREATE TABLE IF NOT EXISTS cron
                 (NAME           VARCHAR(50)   NOT NULL,
                 LASTRUN        DATETIME);''')
        conn.commit()

    def debug_printDB(self):
        global conn
        try:
            cursor = conn.execute("SELECT * FROM cron")
            data=cursor.fetchall()
            for row in data:
                if row != None:
                    print "CRON-DB-Row:", row
        except Exception as err:
            print "Cron error:", err
            pass
