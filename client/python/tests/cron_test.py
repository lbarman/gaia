import unittest
import sys
import os.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
import gaia_client.cron as cron
import gaia_client.constants as constants
from datetime import datetime, timedelta

class TestCron(unittest.TestCase):

    @staticmethod
    def reset_db():
        c = cron.Cron("test", "12h *", db_in_memory=True)
        c.db_truncate()

    def test_cron_create(self):
        print("Testing cron creation")
        self.reset_db()

        # all days
        c = cron.Cron("test", "12h *", db_in_memory=True)

        self.assertEqual(c.hour, 12)
        self.assertEqual(c.days, [0,1,2,3,4,5,6])

        # a subset of days
        c = cron.Cron("test", "01h 1,4,6", db_in_memory=True)
        self.assertEqual(c.hour, 1)
        self.assertEqual(c.days, [1,4,6])

        # a subset of days
        c = cron.Cron("test", "23h 3,1,0", db_in_memory=True)
        self.assertEqual(c.hour, 23)
        self.assertEqual(c.days, [0,1,3])

        with self.assertRaises(ValueError):
            cron.Cron("test", "a *", db_in_memory=True)

        with self.assertRaises(ValueError):
            cron.Cron("test", "-1 *", db_in_memory=True)

        with self.assertRaises(ValueError):
            cron.Cron("test", "1 7", db_in_memory=True)

        c.db_truncate()

    def test_cron_db(self):
        print("Testing cron database")
        self.reset_db()

        # all days
        c = cron.Cron("test", "12h *", db_in_memory=True)

        self.assertEqual(c.last_time_run(), c.time0)

        c.db_truncate()


    def test_cron_run_everyday(self):
        print("Testing cron schedule when run everyday")
        self.reset_db()

        now = datetime.now().replace(day=1,hour=10,minute=30, second=0, microsecond=0)
        c = cron.Cron("test", "12h *", db_in_memory=True)
        self.assertEqual(c.last_time_run(), c.time0)

        # should run in two hours, not now
        self.assertEqual(c.should_it_run(now), False)
        expected = datetime.now().replace(day=1,hour=12,minute=00, second=0, microsecond=0)
        self.assertEqual(c.next_occurrence(now), expected)

        # 30 minutes before, still not
        now = datetime.now().replace(day=1,hour=11,minute=29, second=0, microsecond=0)
        self.assertEqual(c.should_it_run(now), False)
        expected = datetime.now().replace(day=1,hour=12,minute=00, second=0, microsecond=0)
        self.assertEqual(c.next_occurrence(now), expected)

        # 29 minutes before, should run exactly once
        now = datetime.now().replace(day=1,hour=11,minute=31, second=0, microsecond=0)
        expected = datetime.now().replace(day=1,hour=12,minute=00, second=0, microsecond=0)
        self.assertEqual(c.next_occurrence(now), expected)
        self.assertEqual(c.should_it_run(now), True)
        self.assertEqual(c.should_it_run(now), False) #exactly once
        self.assertEqual(c.last_time_run(), expected)

        # then, it should run in 1 day
        expected = datetime.now().replace(day=2,hour=12,minute=00, second=0, microsecond=0)
        self.assertEqual(c.next_occurrence(now), expected)

        # 30 minutes before, still not
        now = datetime.now().replace(day=2,hour=11,minute=29, second=0, microsecond=0)
        self.assertEqual(c.should_it_run(now), False)
        expected = datetime.now().replace(day=2,hour=12,minute=00, second=0, microsecond=0)
        self.assertEqual(c.next_occurrence(now), expected)

        # 29 minutes before, should run exactly once
        now = datetime.now().replace(day=2,hour=11,minute=31, second=0, microsecond=0)
        expected = datetime.now().replace(day=2,hour=12,minute=00, second=0, microsecond=0)
        self.assertEqual(c.next_occurrence(now), expected)
        self.assertEqual(c.should_it_run(now), True)
        self.assertEqual(c.should_it_run(now), False) #exactly once
        self.assertEqual(c.last_time_run(), expected)

        # then, it should run in 1 day
        expected = datetime.now().replace(day=3,hour=12,minute=00, second=0, microsecond=0)
        self.assertEqual(c.next_occurrence(now), expected)

        # awesome, this work. Now test the edge case when the month is january and we're on the 31

        c.db_truncate()
        c = cron.Cron("test", "12h *", db_in_memory=True)

        now = datetime.now().replace(year=2018,month=12,day=31,hour=10,minute=30, second=0, microsecond=0)

        # should run in two hours, not now
        self.assertEqual(c.should_it_run(now), False)
        expected = datetime.now().replace(year=2018,month=12,day=31,hour=12,minute=00, second=0, microsecond=0)
        self.assertEqual(c.next_occurrence(now), expected)

        # 29 minutes before, should run exactly once
        now = datetime.now().replace(year=2018,month=12,day=31,hour=11,minute=31, second=0, microsecond=0)
        expected = datetime.now().replace(year=2018,month=12,day=31,hour=12,minute=00, second=0, microsecond=0)
        self.assertEqual(c.next_occurrence(now), expected)
        self.assertEqual(c.should_it_run(now), True)
        self.assertEqual(c.should_it_run(now), False) #exactly once
        self.assertEqual(c.last_time_run(), expected)

        # then, it should run in 1 day
        expected = datetime.now().replace(year=2019,month=1,day=1,hour=12,minute=00, second=0, microsecond=0)
        self.assertEqual(c.next_occurrence(now), expected)

        c.db_truncate()

    def test_cron_midnight(self):
        print("Testing cron over midnight")
        self.reset_db()

        # all days
        c = cron.Cron("test", "13h 1,4", db_in_memory=True)
        self.assertEqual(c.last_time_run(), c.time0)

        # should run in two hours, not now
        now = datetime.now().replace(year=2018,month=8,day=12,hour=22,minute=29, second=0, microsecond=0)
        self.assertEqual(c.should_it_run(now), False)
        expected = datetime.now().replace(year=2018,month=8,day=14,hour=13,minute=00, second=0, microsecond=0)
        self.assertEqual(c.next_occurrence(now), expected)

        # 1 minute before midnight, nothing changed
        now = datetime.now().replace(year=2018,month=8,day=12,hour=23,minute=59, second=0, microsecond=0)
        self.assertEqual(c.should_it_run(now), False)
        expected = datetime.now().replace(year=2018,month=8,day=14,hour=13,minute=00, second=0, microsecond=0)
        self.assertEqual(c.next_occurrence(now), expected)

        # 1 minute after midnight, nothing changed
        now = datetime.now().replace(year=2018,month=8,day=13,hour=0,minute=1, second=0, microsecond=0)
        self.assertEqual(c.should_it_run(now), False)
        expected = datetime.now().replace(year=2018,month=8,day=14,hour=13,minute=00, second=0, microsecond=0)
        self.assertEqual(c.next_occurrence(now), expected)

        # 1 minute before the next midnight, nothing changed
        now = datetime.now().replace(year=2018,month=8,day=13,hour=23,minute=59, second=0, microsecond=0)
        self.assertEqual(c.should_it_run(now), False)
        expected = datetime.now().replace(year=2018,month=8,day=14,hour=13,minute=00, second=0, microsecond=0)
        self.assertEqual(c.next_occurrence(now), expected)

        # 1 minute after the next midnight, nothing changed
        now = datetime.now().replace(year=2018,month=8,day=14,hour=0,minute=1, second=0, microsecond=0)
        self.assertEqual(c.should_it_run(now), False)
        expected = datetime.now().replace(year=2018,month=8,day=14,hour=13,minute=00, second=0, microsecond=0)
        self.assertEqual(c.next_occurrence(now), expected)

        # 29 minutes before, should run exactly once
        now = datetime.now().replace(year=2018,month=8,day=14,hour=12,minute=31, second=0, microsecond=0)
        expected = datetime.now().replace(year=2018,month=8,day=14,hour=13,minute=00, second=0, microsecond=0)
        self.assertEqual(c.next_occurrence(now), expected)
        self.assertEqual(c.should_it_run(now), True)
        self.assertEqual(c.should_it_run(now), False) #exactly once
        self.assertEqual(c.last_time_run(), expected)

        # then, it should run in 1 day (Friday)
        expected = datetime.now().replace(year=2018,month=8,day=17,hour=13,minute=00, second=0, microsecond=0)
        self.assertEqual(c.next_occurrence(now), expected)

        c.db_truncate()

    def test_cron_run_customschedule(self):
        print("Testing cron schedule when run monday, wednesday, and sunday")
        self.reset_db()

        cron_string = "23h 0,2,6"

        # this is a monday
        now = datetime.now().replace(year=2018,month=7,day=23,hour=10,minute=30, second=0, microsecond=0)
        c = cron.Cron("test", cron_string, db_in_memory=True)
        self.assertEqual(c.last_time_run(), c.time0)

        # should run in two hours, not now
        self.assertEqual(c.should_it_run(now), False)
        expected = datetime.now().replace(year=2018,month=7,day=23,hour=23,minute=00, second=0, microsecond=0)
        self.assertEqual(c.next_occurrence(now), expected)

        # 30 minutes before, still not
        now = datetime.now().replace(year=2018,month=7,day=23,hour=22,minute=29, second=0, microsecond=0)
        self.assertEqual(c.should_it_run(now), False)
        expected = datetime.now().replace(year=2018,month=7,day=23,hour=23,minute=00, second=0, microsecond=0)
        self.assertEqual(c.next_occurrence(now), expected)

        # 29 minutes before, should run exactly once
        now = datetime.now().replace(year=2018,month=7,day=23,hour=22,minute=31, second=0, microsecond=0)
        expected = datetime.now().replace(year=2018,month=7,day=23,hour=23,minute=00, second=0, microsecond=0)
        self.assertEqual(c.next_occurrence(now), expected)
        self.assertEqual(c.should_it_run(now), True)
        self.assertEqual(c.should_it_run(now), False) #exactly once
        self.assertEqual(c.last_time_run(), expected)

        # then, it should run in 2 days, on wednesday
        expected = datetime.now().replace(year=2018,month=7,day=25,hour=23,minute=00, second=0, microsecond=0)
        self.assertEqual(c.next_occurrence(now), expected)

        # 30 minutes before, still not
        now = datetime.now().replace(year=2018,month=7,day=25,hour=22,minute=29, second=0, microsecond=0)
        self.assertEqual(c.should_it_run(now), False)
        expected = datetime.now().replace(year=2018,month=7,day=25,hour=23,minute=00, second=0, microsecond=0)
        self.assertEqual(c.next_occurrence(now), expected)

        # 29 minutes before, should run exactly once
        now = datetime.now().replace(year=2018,month=7,day=25,hour=22,minute=31, second=0, microsecond=0)
        expected = datetime.now().replace(year=2018,month=7,day=25,hour=23,minute=00, second=0, microsecond=0)
        self.assertEqual(c.next_occurrence(now), expected)
        self.assertEqual(c.should_it_run(now), True)
        self.assertEqual(c.should_it_run(now), False) #exactly once
        self.assertEqual(c.last_time_run(), expected)

        # then, it should run in 4 day (Sunday)
        expected = datetime.now().replace(year=2018,month=7,day=29,hour=23,minute=00, second=0, microsecond=0)
        self.assertEqual(c.next_occurrence(now), expected)

        # 29 minutes before, should run exactly once
        now = datetime.now().replace(year=2018,month=7,day=29,hour=22,minute=31, second=0, microsecond=0)
        expected = datetime.now().replace(year=2018,month=7,day=29,hour=23,minute=00, second=0, microsecond=0)
        self.assertEqual(c.next_occurrence(now), expected)
        self.assertEqual(c.should_it_run(now), True)
        self.assertEqual(c.should_it_run(now), False) #exactly once
        self.assertEqual(c.last_time_run(), expected)

        # then, it should run in 1 day (Monday)
        expected = datetime.now().replace(year=2018,month=7,day=30,hour=23,minute=00, second=0, microsecond=0)
        self.assertEqual(c.next_occurrence(now), expected)

        c.db_truncate()


    def test_cron_run_customschedule2(self):
        print("Testing cron schedule when run every saturday")
        self.reset_db()

        cron_string = "0h 5" #midnight on friday (00:00 saturday)

        # this is a monday
        now = datetime.now().replace(year=2018,month=12,day=27,hour=10,minute=30, second=0, microsecond=0)
        c = cron.Cron("test", cron_string, db_in_memory=True)

        # should run in two hours, not now
        self.assertEqual(c.should_it_run(now), False)
        expected = datetime.now().replace(year=2018,month=12,day=29,hour=00,minute=00, second=0, microsecond=0)
        self.assertEqual(c.next_occurrence(now), expected)

        # 30 minutes before, still not
        now = datetime.now().replace(year=2018,month=12,day=28,hour=23,minute=29, second=0, microsecond=0)
        self.assertEqual(c.should_it_run(now), False)
        expected = datetime.now().replace(year=2018,month=12,day=29,hour=00,minute=00, second=0, microsecond=0)
        self.assertEqual(c.next_occurrence(now), expected)

        # 29 minutes before, should run exactly once
        now = datetime.now().replace(year=2018,month=12,day=28,hour=23,minute=31, second=0, microsecond=0)
        expected = datetime.now().replace(year=2018,month=12,day=29,hour=00,minute=00, second=0, microsecond=0)
        self.assertEqual(c.next_occurrence(now), expected)
        self.assertEqual(c.should_it_run(now), True)
        self.assertEqual(c.should_it_run(now), False) #exactly once

        # then, it should run in 7 days, on saturday
        expected = datetime.now().replace(year=2019,month=1,day=5,hour=0,minute=0, second=0, microsecond=0)
        self.assertEqual(c.next_occurrence(now), expected)

        # 30 minutes before, still not
        now = datetime.now().replace(year=2019,month=1,day=4,hour=23,minute=29, second=0, microsecond=0)
        self.assertEqual(c.should_it_run(now), False)
        expected = datetime.now().replace(year=2019,month=1,day=5,hour=0,minute=00, second=0, microsecond=0)
        self.assertEqual(c.next_occurrence(now), expected)

        # 29 minutes before, should run exactly once
        now = datetime.now().replace(year=2019,month=1,day=4,hour=23,minute=31, second=0, microsecond=0)
        expected = datetime.now().replace(year=2019,month=1,day=5,hour=0,minute=00, second=0, microsecond=0)
        self.assertEqual(c.next_occurrence(now), expected)
        self.assertEqual(c.should_it_run(now), True)
        self.assertEqual(c.should_it_run(now), False) #exactly once

        # then, it should run in 7 day (next saturday)
        expected = datetime.now().replace(year=2019,month=1,day=12,hour=0,minute=00, second=0, microsecond=0)
        self.assertEqual(c.next_occurrence(now), expected)

        # 29 minutes before, should run exactly once
        now = datetime.now().replace(year=2019,month=1,day=11,hour=23,minute=31, second=0, microsecond=0)
        expected = datetime.now().replace(year=2019,month=1,day=12,hour=0,minute=00, second=0, microsecond=0)
        self.assertEqual(c.next_occurrence(now), expected)
        self.assertEqual(c.should_it_run(now), True)
        self.assertEqual(c.should_it_run(now), False) #exactly once

        # then, it should run in 7 days
        expected = datetime.now().replace(year=2019,month=1,day=19,hour=00,minute=00, second=0, microsecond=0)
        self.assertEqual(c.next_occurrence(now), expected)

        c.db_truncate()


    # should not run between time [begin;target[
    # should run exactly once at target, and not anymore before end
    # DB state should change exactly once
    def nextCronShouldOccur(self, cron, last_day_executed, begin, target, end):

        ticks_seconds = constants.WAITING_LOOP_SLEEP

        # lastDayExecuted must be provided correctly
        self.assertEqual(cron.last_time_run(), last_day_executed)

        now = begin

        # during that time span, should NOT run
        # DB should not change
        while now<=(target - timedelta(minutes=cron.window_before_deadline)):
            self.assertEqual(cron.last_time_run(), last_day_executed)
            self.assertEqual(cron.should_it_run(now), False)
            self.assertEqual(cron.next_occurrence(now), target)

            now = now + timedelta(seconds=ticks_seconds)

        # now, should run exactly once, at the expected time
        self.assertEqual(cron.next_occurrence(now), target)
        self.assertEqual(cron.should_it_run(now), True)
        self.assertEqual(cron.should_it_run(now), False)

        # should *not* run again
        while now<end:
            self.assertEqual(cron.last_time_run(), target)
            self.assertEqual(cron.should_it_run(now), False)
            now = now + timedelta(seconds=ticks_seconds)


    def test_cron_run_everyday_2(self):
        print("Testing cron schedule when run everyday :")
        self.reset_db()
        c = cron.Cron("test", "12h *", db_in_memory=True)
        last_run = c.time0

        day = 1
        while day < 30:
            start  = datetime.now().replace(day=day,hour=10,minute=30, second=0, microsecond=0)
            target = datetime.now().replace(day=day,hour=12,minute=00, second=0, microsecond=0)
            end    = datetime.now().replace(day=(day+1),hour=11,minute=29, second=0, microsecond=0)
            print("Testing for", target)
            self.nextCronShouldOccur(c, last_run, start, target, end)
            last_run = target

            day += 1

        c.db_truncate()

    def test_cron_run_custom_schedule(self):
        print("Testing cron schedule when run monday, wednesday, and sunday")
        self.reset_db()

        c = cron.Cron("test", "23h 0,2,6", db_in_memory=True)
        last_run = c.time0

        day = 23
        while day < 30:
            start  = datetime.now().replace(year=2018,month=7,day=day,hour=20,minute=30, second=0, microsecond=0)
            target = datetime.now().replace(year=2018,month=7,day=day,hour=23,minute=00, second=0, microsecond=0)
            end    = datetime.now().replace(year=2018,month=7,day=(day+1),hour=22,minute=29, second=0, microsecond=0)
            print("Testing for", target)
            self.nextCronShouldOccur(c, last_run, start, target, end)
            last_run = target

            day += 1
            # skip tuesday, thursday, friday, saturday
            while day == 24 or day == 26 or day == 27 or day == 28:
                day += 1

        day = 1
        while day < 12:
            start  = datetime.now().replace(year=2018,month=8,day=day,hour=20,minute=30, second=0, microsecond=0)
            target = datetime.now().replace(year=2018,month=8,day=day,hour=23,minute=00, second=0, microsecond=0)
            end    = datetime.now().replace(year=2018,month=8,day=(day+1),hour=22,minute=29, second=0, microsecond=0)
            print("Testing for", target)
            self.nextCronShouldOccur(c, last_run, start, target, end)
            last_run = target

            day += 1
            # skip tuesday, thursday, friday, saturday
            while day == 2 or day == 3 or day == 4 or day == 7 or day == 9 or day == 10 or day == 11:
                day += 1

        c.db_truncate()

    def test_cron_run_over_new_year(self):
        print("Testing cron schedule when run monday, thursday")
        self.reset_db()

        c = cron.Cron("test", "0h 1,4", db_in_memory=True) #midnight on monday (00:00 tuesday) and thursday (00:00 friday)
        last_run = c.time0

        day = 24
        while day < 29:
            start  = datetime.now().replace(year=2018,month=12,day=day,hour=22,minute=30, second=0, microsecond=0)
            target = datetime.now().replace(year=2018,month=12,day=(day+1),hour=00,minute=00, second=0, microsecond=0)
            end    = datetime.now().replace(year=2018,month=12,day=(day+1),hour=22,minute=29, second=0, microsecond=0)
            print("Testing for", target)
            self.nextCronShouldOccur(c, last_run, start, target, end)
            last_run = target

            day += 1
            # skip monday, wednesday, friday, sunday
            while day == 25 or day == 26 or day == 28 or day == 29:
                day += 1

        day = 3
        while day < 11:
            start  = datetime.now().replace(year=2019,month=1,day=day,hour=22,minute=30, second=0, microsecond=0)
            target = datetime.now().replace(year=2019,month=1,day=(day+1),hour=00,minute=00, second=0, microsecond=0)
            end    = datetime.now().replace(year=2019,month=1,day=(day+1),hour=22,minute=29, second=0, microsecond=0)
            print("Testing for", target)
            self.nextCronShouldOccur(c, last_run, start, target, end)
            last_run = target

            day += 1
            # skip tuesday, thursday, friday, saturday
            while day == 4 or day == 5 or day == 6 or day == 8 or day == 9:
                day += 1

        c.db_truncate()

if __name__ == '__main__':
    unittest.main()
