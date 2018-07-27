import unittest
from cron import Cron
import datetime

class TestCron(unittest.TestCase):

    def dbReset(self):
        c = Cron("test", "12 *", sqliteMemoryMode=True)
        c.debug_truncateDB()

    def test_cron_create(self):
        print "Testing cron creation"
        self.dbReset()

        # all days
        c = Cron("test", "12 *", sqliteMemoryMode=True)

        self.assertEqual(c.hour, 12)
        self.assertEqual(c.days, [0,1,2,3,4,5,6])

        # a subset of days
        c = Cron("test", "01 1,4,6", sqliteMemoryMode=True)
        self.assertEqual(c.hour, 1)
        self.assertEqual(c.days, [1,4,6])

        # a subset of days
        c = Cron("test", "23 3,1,0", sqliteMemoryMode=True)
        self.assertEqual(c.hour, 23)
        self.assertEqual(c.days, [0,1,3])

        with self.assertRaises(ValueError):
            c = Cron("test", "a *", sqliteMemoryMode=True)

        with self.assertRaises(ValueError):
            c = Cron("test", "-1 *", sqliteMemoryMode=True)

        with self.assertRaises(ValueError):
            c = Cron("test", "1 7", sqliteMemoryMode=True)

        c.debug_truncateDB()

    def test_cron_db(self):
        print "Testing cron database"
        self.dbReset()

        # all days
        c = Cron("test", "12 *", sqliteMemoryMode=True)

        self.assertEqual(c.lastDayExecuted(), c.time0)

        c.debug_truncateDB()


    def test_cron_run_everyday(self):
        print "Testing cron schedule when run everyday"
        self.dbReset()

        now = datetime.datetime.now().replace(day=1,hour=10,minute=30, second=0, microsecond=0)
        c = Cron("test", "12 *", sqliteMemoryMode=True)
        self.assertEqual(c.lastDayExecuted(), c.time0)

        # should run in two hours, not now
        self.assertEqual(c.shouldItRun(now), False)
        expected = datetime.datetime.now().replace(day=1,hour=12,minute=00, second=0, microsecond=0)
        self.assertEqual(c.nextOccurence(now), expected)

        # 30 minutes before, still not
        now = datetime.datetime.now().replace(day=1,hour=11,minute=29, second=0, microsecond=0)
        self.assertEqual(c.shouldItRun(now), False)
        expected = datetime.datetime.now().replace(day=1,hour=12,minute=00, second=0, microsecond=0)
        self.assertEqual(c.nextOccurence(now), expected)

        # 29 minutes before, should run exactly once
        now = datetime.datetime.now().replace(day=1,hour=11,minute=31, second=0, microsecond=0)
        expected = datetime.datetime.now().replace(day=1,hour=12,minute=00, second=0, microsecond=0)
        self.assertEqual(c.nextOccurence(now), expected)
        self.assertEqual(c.shouldItRun(now), True)
        self.assertEqual(c.shouldItRun(now), False) #exactly once
        self.assertEqual(c.lastDayExecuted(), expected)

        # then, it should run in 1 day
        expected = datetime.datetime.now().replace(day=2,hour=12,minute=00, second=0, microsecond=0)
        self.assertEqual(c.nextOccurence(now), expected)

        # 30 minutes before, still not
        now = datetime.datetime.now().replace(day=2,hour=11,minute=29, second=0, microsecond=0)
        self.assertEqual(c.shouldItRun(now), False)
        expected = datetime.datetime.now().replace(day=2,hour=12,minute=00, second=0, microsecond=0)
        self.assertEqual(c.nextOccurence(now), expected)

        # 29 minutes before, should run exactly once
        now = datetime.datetime.now().replace(day=2,hour=11,minute=31, second=0, microsecond=0)
        expected = datetime.datetime.now().replace(day=2,hour=12,minute=00, second=0, microsecond=0)
        self.assertEqual(c.nextOccurence(now), expected)
        self.assertEqual(c.shouldItRun(now), True)
        self.assertEqual(c.shouldItRun(now), False) #exactly once
        self.assertEqual(c.lastDayExecuted(), expected)

        # then, it should run in 1 day
        expected = datetime.datetime.now().replace(day=3,hour=12,minute=00, second=0, microsecond=0)
        self.assertEqual(c.nextOccurence(now), expected)

        # awesome, this work. Now test the edge case when the month is january and we're on the 31

        c.debug_truncateDB()
        c = Cron("test", "12 *", sqliteMemoryMode=True)

        now = datetime.datetime.now().replace(year=2018,month=12,day=31,hour=10,minute=30, second=0, microsecond=0)

        # should run in two hours, not now
        self.assertEqual(c.shouldItRun(now), False)
        expected = datetime.datetime.now().replace(year=2018,month=12,day=31,hour=12,minute=00, second=0, microsecond=0)
        self.assertEqual(c.nextOccurence(now), expected)

        # 29 minutes before, should run exactly once
        now = datetime.datetime.now().replace(year=2018,month=12,day=31,hour=11,minute=31, second=0, microsecond=0)
        expected = datetime.datetime.now().replace(year=2018,month=12,day=31,hour=12,minute=00, second=0, microsecond=0)
        self.assertEqual(c.nextOccurence(now), expected)
        self.assertEqual(c.shouldItRun(now), True)
        self.assertEqual(c.shouldItRun(now), False) #exactly once
        self.assertEqual(c.lastDayExecuted(), expected)

        # then, it should run in 1 day
        expected = datetime.datetime.now().replace(year=2019,month=1,day=1,hour=12,minute=00, second=0, microsecond=0)
        self.assertEqual(c.nextOccurence(now), expected)

        c.debug_truncateDB()

    def test_cron_run_customschedule(self):
        print "Testing cron schedule when run monday, wednesday, and sunday"
        self.dbReset()

        cronString = "23 0,2,6"

        # this is a monday
        now = datetime.datetime.now().replace(year=2018,month=7,day=23,hour=10,minute=30, second=0, microsecond=0)
        c = Cron("test", cronString, sqliteMemoryMode=True)
        self.assertEqual(c.lastDayExecuted(), c.time0)

        # should run in two hours, not now
        self.assertEqual(c.shouldItRun(now), False)
        expected = datetime.datetime.now().replace(year=2018,month=7,day=23,hour=23,minute=00, second=0, microsecond=0)
        self.assertEqual(c.nextOccurence(now), expected)

        # 30 minutes before, still not
        now = datetime.datetime.now().replace(year=2018,month=7,day=23,hour=22,minute=29, second=0, microsecond=0)
        self.assertEqual(c.shouldItRun(now), False)
        expected = datetime.datetime.now().replace(year=2018,month=7,day=23,hour=23,minute=00, second=0, microsecond=0)
        self.assertEqual(c.nextOccurence(now), expected)

        # 29 minutes before, should run exactly once
        now = datetime.datetime.now().replace(year=2018,month=7,day=23,hour=22,minute=31, second=0, microsecond=0)
        expected = datetime.datetime.now().replace(year=2018,month=7,day=23,hour=23,minute=00, second=0, microsecond=0)
        self.assertEqual(c.nextOccurence(now), expected)
        self.assertEqual(c.shouldItRun(now), True)
        self.assertEqual(c.shouldItRun(now), False) #exactly once
        self.assertEqual(c.lastDayExecuted(), expected)

        # then, it should run in 2 days, on wednesday
        expected = datetime.datetime.now().replace(year=2018,month=7,day=25,hour=23,minute=00, second=0, microsecond=0)
        self.assertEqual(c.nextOccurence(now), expected)

        # 30 minutes before, still not
        now = datetime.datetime.now().replace(year=2018,month=7,day=25,hour=22,minute=29, second=0, microsecond=0)
        self.assertEqual(c.shouldItRun(now), False)
        expected = datetime.datetime.now().replace(year=2018,month=7,day=25,hour=23,minute=00, second=0, microsecond=0)
        self.assertEqual(c.nextOccurence(now), expected)

        # 29 minutes before, should run exactly once
        now = datetime.datetime.now().replace(year=2018,month=7,day=25,hour=22,minute=31, second=0, microsecond=0)
        expected = datetime.datetime.now().replace(year=2018,month=7,day=25,hour=23,minute=00, second=0, microsecond=0)
        self.assertEqual(c.nextOccurence(now), expected)
        self.assertEqual(c.shouldItRun(now), True)
        self.assertEqual(c.shouldItRun(now), False) #exactly once
        self.assertEqual(c.lastDayExecuted(), expected)

        # then, it should run in 4 day (Sunday)
        expected = datetime.datetime.now().replace(year=2018,month=7,day=29,hour=23,minute=00, second=0, microsecond=0)
        self.assertEqual(c.nextOccurence(now), expected)

        # 29 minutes before, should run exactly once
        now = datetime.datetime.now().replace(year=2018,month=7,day=29,hour=22,minute=31, second=0, microsecond=0)
        expected = datetime.datetime.now().replace(year=2018,month=7,day=29,hour=23,minute=00, second=0, microsecond=0)
        self.assertEqual(c.nextOccurence(now), expected)
        self.assertEqual(c.shouldItRun(now), True)
        self.assertEqual(c.shouldItRun(now), False) #exactly once
        self.assertEqual(c.lastDayExecuted(), expected)

        # then, it should run in 1 day (Monday)
        expected = datetime.datetime.now().replace(year=2018,month=7,day=30,hour=23,minute=00, second=0, microsecond=0)
        self.assertEqual(c.nextOccurence(now), expected)

        c.debug_truncateDB()


    def test_cron_run_customschedule(self):
        print "Testing cron schedule when run monday, wednesday, and sunday"
        self.dbReset()

        cronString = "23 0,2,6"

        # this is a monday
        now = datetime.datetime.now().replace(year=2018,month=7,day=23,hour=10,minute=30, second=0, microsecond=0)
        c = Cron("test", cronString, sqliteMemoryMode=True)
        self.assertEqual(c.lastDayExecuted(), c.time0)

        # should run in two hours, not now
        self.assertEqual(c.shouldItRun(now), False)
        expected = datetime.datetime.now().replace(year=2018,month=7,day=23,hour=23,minute=00, second=0, microsecond=0)
        self.assertEqual(c.nextOccurence(now), expected)

        # 30 minutes before, still not
        now = datetime.datetime.now().replace(year=2018,month=7,day=23,hour=22,minute=29, second=0, microsecond=0)
        self.assertEqual(c.shouldItRun(now), False)
        expected = datetime.datetime.now().replace(year=2018,month=7,day=23,hour=23,minute=00, second=0, microsecond=0)
        self.assertEqual(c.nextOccurence(now), expected)

        # 29 minutes before, should run exactly once
        now = datetime.datetime.now().replace(year=2018,month=7,day=23,hour=22,minute=31, second=0, microsecond=0)
        expected = datetime.datetime.now().replace(year=2018,month=7,day=23,hour=23,minute=00, second=0, microsecond=0)
        self.assertEqual(c.nextOccurence(now), expected)
        self.assertEqual(c.shouldItRun(now), True)
        self.assertEqual(c.shouldItRun(now), False) #exactly once
        self.assertEqual(c.lastDayExecuted(), expected)

        # then, it should run in 2 days, on wednesday
        expected = datetime.datetime.now().replace(year=2018,month=7,day=25,hour=23,minute=00, second=0, microsecond=0)
        self.assertEqual(c.nextOccurence(now), expected)

        # 30 minutes before, still not
        now = datetime.datetime.now().replace(year=2018,month=7,day=25,hour=22,minute=29, second=0, microsecond=0)
        self.assertEqual(c.shouldItRun(now), False)
        expected = datetime.datetime.now().replace(year=2018,month=7,day=25,hour=23,minute=00, second=0, microsecond=0)
        self.assertEqual(c.nextOccurence(now), expected)

        # 29 minutes before, should run exactly once
        now = datetime.datetime.now().replace(year=2018,month=7,day=25,hour=22,minute=31, second=0, microsecond=0)
        expected = datetime.datetime.now().replace(year=2018,month=7,day=25,hour=23,minute=00, second=0, microsecond=0)
        self.assertEqual(c.nextOccurence(now), expected)
        self.assertEqual(c.shouldItRun(now), True)
        self.assertEqual(c.shouldItRun(now), False) #exactly once
        self.assertEqual(c.lastDayExecuted(), expected)

        # then, it should run in 4 day (Sunday)
        expected = datetime.datetime.now().replace(year=2018,month=7,day=29,hour=23,minute=00, second=0, microsecond=0)
        self.assertEqual(c.nextOccurence(now), expected)

        # 29 minutes before, should run exactly once
        now = datetime.datetime.now().replace(year=2018,month=7,day=29,hour=22,minute=31, second=0, microsecond=0)
        expected = datetime.datetime.now().replace(year=2018,month=7,day=29,hour=23,minute=00, second=0, microsecond=0)
        self.assertEqual(c.nextOccurence(now), expected)
        self.assertEqual(c.shouldItRun(now), True)
        self.assertEqual(c.shouldItRun(now), False) #exactly once
        self.assertEqual(c.lastDayExecuted(), expected)

        # then, it should run in 1 day (Monday)
        expected = datetime.datetime.now().replace(year=2018,month=7,day=30,hour=23,minute=00, second=0, microsecond=0)
        self.assertEqual(c.nextOccurence(now), expected)

        c.debug_truncateDB()




    def test_cron_run_customschedule2(self):
        print "Testing cron schedule when run every saturday"
        self.dbReset()

        cronString = "0 5" #midnight on friday (00:00 saturday)

        # this is a monday
        now = datetime.datetime.now().replace(year=2018,month=12,day=27,hour=10,minute=30, second=0, microsecond=0)
        c = Cron("test", cronString, sqliteMemoryMode=True)

        # should run in two hours, not now
        self.assertEqual(c.shouldItRun(now), False)
        expected = datetime.datetime.now().replace(year=2018,month=12,day=29,hour=00,minute=00, second=0, microsecond=0)
        self.assertEqual(c.nextOccurence(now), expected)

        # 30 minutes before, still not
        now = datetime.datetime.now().replace(year=2018,month=12,day=28,hour=23,minute=29, second=0, microsecond=0)
        self.assertEqual(c.shouldItRun(now), False)
        expected = datetime.datetime.now().replace(year=2018,month=12,day=29,hour=00,minute=00, second=0, microsecond=0)
        self.assertEqual(c.nextOccurence(now), expected)

        # 29 minutes before, should run exactly once
        now = datetime.datetime.now().replace(year=2018,month=12,day=28,hour=23,minute=31, second=0, microsecond=0)
        expected = datetime.datetime.now().replace(year=2018,month=12,day=29,hour=00,minute=00, second=0, microsecond=0)
        self.assertEqual(c.nextOccurence(now), expected)
        self.assertEqual(c.shouldItRun(now), True)
        self.assertEqual(c.shouldItRun(now), False) #exactly once

        # then, it should run in 7 days, on saturday
        expected = datetime.datetime.now().replace(year=2019,month=1,day=05,hour=0,minute=00, second=0, microsecond=0)
        self.assertEqual(c.nextOccurence(now), expected)

        # 30 minutes before, still not
        now = datetime.datetime.now().replace(year=2019,month=1,day=04,hour=23,minute=29, second=0, microsecond=0)
        self.assertEqual(c.shouldItRun(now), False)
        expected = datetime.datetime.now().replace(year=2019,month=1,day=05,hour=0,minute=00, second=0, microsecond=0)
        self.assertEqual(c.nextOccurence(now), expected)

        # 29 minutes before, should run exactly once
        now = datetime.datetime.now().replace(year=2019,month=1,day=04,hour=23,minute=31, second=0, microsecond=0)
        expected = datetime.datetime.now().replace(year=2019,month=1,day=05,hour=0,minute=00, second=0, microsecond=0)
        self.assertEqual(c.nextOccurence(now), expected)
        self.assertEqual(c.shouldItRun(now), True)
        self.assertEqual(c.shouldItRun(now), False) #exactly once

        # then, it should run in 7 day (next saturday)
        expected = datetime.datetime.now().replace(year=2019,month=1,day=12,hour=0,minute=00, second=0, microsecond=0)
        self.assertEqual(c.nextOccurence(now), expected)

        # 29 minutes before, should run exactly once
        now = datetime.datetime.now().replace(year=2019,month=1,day=11,hour=23,minute=31, second=0, microsecond=0)
        expected = datetime.datetime.now().replace(year=2019,month=1,day=12,hour=0,minute=00, second=0, microsecond=0)
        self.assertEqual(c.nextOccurence(now), expected)
        self.assertEqual(c.shouldItRun(now), True)
        self.assertEqual(c.shouldItRun(now), False) #exactly once

        # then, it should run in 7 days
        expected = datetime.datetime.now().replace(year=2019,month=1,day=19,hour=00,minute=00, second=0, microsecond=0)
        self.assertEqual(c.nextOccurence(now), expected)

        c.debug_truncateDB()

unittest.main()