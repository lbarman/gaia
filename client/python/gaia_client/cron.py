from datetime import datetime, timedelta
import gaia_client.constants as constants
import sqlite3
import re


# Cron string with format "h x,y,z" means "at X o'clock every x/y/z day of the week"
class Cron:

    time0 = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0, day=1, month=1, year=1970)
    cron_name = "unknown"
    cron_string = ""
    hour = ""
    days = []
    db = None

    # a Cron task runs exactly once in [target-CRON_WINDOW_BEFORE_DEADLINE; target] if called during that time
    def __init__(self, cron_name, cron_string, db_in_memory=False, window_before_deadline=30):

        # recreate the database
        db_file = constants.SQLITE_FILE
        if db_in_memory:
            db_file = ':memory:'

        self.db = sqlite3.connect(db_file, detect_types=sqlite3.PARSE_DECLTYPES)

        # sanity check
        pattern = re.compile(constants.CRON_REGEX_TESTER)
        if not pattern.match(cron_string):
            raise ValueError('Cron string is invalid:', cron_string)

        # then, create this Cron. Parse the data and standardize it
        self.cron_name = cron_name
        self.cron_string = cron_string
        self.window_before_deadline = window_before_deadline

        parts = self.cron_string.split(" ")
        if len(parts) != 2:
            raise ValueError("Invalid cron string:" + self.cron_string)

        hour = parts[0].strip().replace('h', '')
        days = parts[1].strip()

        if not hour.isdigit():
            raise ValueError("Hour not valid:" + hour)

        self.hour = int(hour)

        if days == "*":
            days = "0,1,2,3,4,5,6"

        days_array = days.split(",")

        self.days = [int(day) for day in days_array]
        self.days = sorted(self.days)

        for day in self.days:
            if day < 0 or day > 6:
                raise ValueError("Day not valid:" + str(day))

        # make sure there is something in the DB w.r.t to this cron
        self.db_recreate()

    def __str__(self):
        return str(self.hour)+"h on "+','.join([constants.DAYS_STRING[x] for x in self.days])

    def next_occurrence(self, now):
        next_occurrence = self.__next_occurrence_irrespective_to_last_run(now)
        last_run = self.last_time_run()

        if next_occurrence == last_run:
            return self.__next_occurrence_irrespective_to_last_run(last_run)

        return next_occurrence

    def __next_occurrence_irrespective_to_last_run(self, now):

        beginning_of_today = now.replace(hour=0, minute=0, second=0, microsecond=0)

        # compute the beginning of the week
        beginning_of_the_week = beginning_of_today
        while beginning_of_the_week.weekday() != 0:
            beginning_of_the_week = beginning_of_the_week - timedelta(days=1)

        # now replace with the time where the cron should run
        monday_at_correct_hour = beginning_of_the_week.replace(hour=self.hour)

        next_run = monday_at_correct_hour

        # increase days by 1 while in the past (we're looking for the next run)
        while next_run <= now:
            next_run = next_run + timedelta(days=1)

        # now that 'next_run' is in the future, continue increasing until finding an allowed day
        while next_run.weekday() not in self.days:
            next_run = next_run + timedelta(days=1)

        return next_run

    def last_time_run(self):
        return self.db_read()

    # we run 30min before the deadline
    # if true, run the action
    # State Machine:
    #    IF: next target is closer than CRON_WINDOW_BEFORE_DEADLINE
    #       IF: last_run is not within [next target - CRON_WINDOW_BEFORE_DEADLINE; now]
    #           run, set last_run to target
    #       ELSE: do nothing
    #    ELSE: do nothing
    def should_it_run(self, now):

        next_occurrence = self.next_occurrence(now)
        last_time_run = self.last_time_run()

        # difference in minutes between now and when it should run
        diff = next_occurrence - now
        diff_until_next_deadline = (diff.total_seconds() / 60)
        
        # difference in minutes between last run and when it should run
        diff = next_occurrence - last_time_run
        diff_last_run_until_next_deadline = (diff.total_seconds() / 60)
        
        # print "diff min", diff_minutes
        # print "last Run and next occurrence diff", diff, diff_minutes2
        
        # if: next execution is soon, CHECK: last execution must be a long time ago
        if diff_until_next_deadline < self.window_before_deadline <= diff_last_run_until_next_deadline:
            self.db_update(next_occurrence)
            return True

        return False

    def db_read(self):
        cursor = self.db.execute('SELECT last_run FROM cron WHERE NAME = (?)', (self.cron_name,))
        data = cursor.fetchone()
        return datetime.strptime(data[0], "%Y-%m-%d %H:%M:%S")

    def db_update(self, last_run):
        self.db.execute('UPDATE cron SET last_run=(?) WHERE name=(?)', (last_run, self.cron_name,))
        self.db.commit()

    def db_recreate(self):
        self.db.execute('CREATE TABLE IF NOT EXISTS cron\n'
                        '                 (name           VARCHAR(50)   NOT NULL,\n'
                        '                  last_run        DATETIME);')
        self.db.commit()

        query = self.db.execute('SELECT count(*) FROM cron').fetchone()

        if query[0] == 0:
            self.db.execute("INSERT INTO cron (name, last_run) VALUES ((?), (?))", (self.cron_name, self.time0,))
            self.db.commit()

    def db_truncate(self):
        self.db.execute('DROP TABLE cron;')
        self.db.commit()

    def db_print(self):
        s = ""
        try:
            cursor = self.db.execute('SELECT * FROM cron')
            data = cursor.fetchall()
            for row in data:
                if row is not None:
                    print("CRON-DB-Row:", row)
                    s += str(row) + '\n'
        except Exception as err:
            print("Cron error:", err)
            s += str(err) + '\n'
            pass
        return s
