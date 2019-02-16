import unittest
import sys
import os.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
import gaia_client.cron_with_default as cron
import gaia_client.database as database
import gaia_client.constants as constants
import gaia_client.protobufs_pb2 as protobufs_pb2

def dummy_config():
    config = protobufs_pb2.Config()
    config.feeding_module_activated = True
    config.watering_module_activated = True
    config.feeding_module_cronstring = "23h 2,3"
    config.watering_module_cronstring = "23h 1,3,5"
    config.watering_pump_1_duration = 10
    config.watering_pump_2_duration = 20
    config.watering_pump_3_duration = 30
    config.watering_pump_4_duration = 40
    return config

def count_records(table, cursor):
    query = cursor.execute('SELECT count(*) FROM ' + table).fetchone()

    if query is None or len(query) == 0:
        return 0

    return query[0]

class TestCronWithDefault(unittest.TestCase):

    def test_cron_create(self):

        db = database.Database(in_memory=True)

        # cron_name must absolutely be "watering_cron" or "feeding_cron"
        with self.assertRaises(ValueError):
            c = cron.CronWithDefault(cron_name="test", cron_string_default="", db=db)

        with self.assertRaises(ValueError):
            c = cron.CronWithDefault(cron_name="watering_cron", cron_string_default="", db=db)

        with self.assertRaises(ValueError):
            c = cron.CronWithDefault(cron_name="watering_cron", cron_string_default=" ", db=db)

        with self.assertRaises(ValueError):
            c = cron.CronWithDefault(cron_name="watering_cron", cron_string_default=None, db=db)

        c = cron.CronWithDefault(cron_name="watering_cron", cron_string_default="12h *", db=db)
        self.assertEqual(c.cron_string, "12h *")

    def test_table_deleted(self):
        config = dummy_config()
        db = database.Database(in_memory=True)
        db.recreate_database()
        db.save_config(config)

        c = cron.CronWithDefault(cron_name="watering_cron", cron_string_default="12h *", db=db)
        self.assertEqual(c.cron_string, "23h 1,3,5")

        db.cursor.execute('DROP TABLE current_config')

        c = cron.CronWithDefault(cron_name="watering_cron", cron_string_default="14h 1,2,3,4,5,6", db=db)
        self.assertEqual(c.cron_string, "14h 1,2,3,4,5,6")

    def test_table_contains_wrong_value(self):
        config = dummy_config()
        config.watering_module_cronstring = "abc"
        db = database.Database(in_memory=True)
        db.recreate_database()
        db.save_config(config)

        c = cron.CronWithDefault(cron_name="watering_cron", cron_string_default="14h 1,2,3,4,5,6", db=db)
        self.assertEqual(c.cron_string, "14h 1,2,3,4,5,6")

        db.cursor.execute('UPDATE current_config SET watering_module_cronstring="12h *"')

        c = cron.CronWithDefault(cron_name="watering_cron", cron_string_default="14h 1,2,3,4,5,6", db=db)
        self.assertEqual(c.cron_string, "12h *")

    def test_feeding(self):
        config = dummy_config()
        config.feeding_module_cronstring = "23h 1,2,3"
        db = database.Database(in_memory=True)
        db.recreate_database()
        db.save_config(config)

        c = cron.FeedingCron(db=db)
        self.assertEqual(c.cron_string, "23h 1,2,3")

        db.cursor.execute('DELETE FROM current_config')

        c = cron.FeedingCron(db=db)
        self.assertEqual(c.cron_string, constants.FEEDING_DEFAULT_CRONSTRING)

    def test_watering(self):
        config = dummy_config()
        config.watering_module_cronstring = "23h 1,2,3"
        db = database.Database(in_memory=True)
        db.recreate_database()
        db.save_config(config)

        c = cron.WateringCron(db=db)
        self.assertEqual(c.cron_string, "23h 1,2,3")

        db.cursor.execute('DELETE FROM current_config')

        c = cron.WateringCron(db=db)
        self.assertEqual(c.cron_string, constants.WATERING_DEFAULT_CRONSTRING)

    def test_enabled_disabled(self):
        db = database.Database(in_memory=True)
        db.recreate_database()

        c = cron.CronWithDefault(cron_name="watering_cron", cron_string_default="14h 1,2,3,4,5,6", cron_enabled=True, db=db)
        self.assertEqual(c.cron_string, "14h 1,2,3,4,5,6")
        self.assertEqual(c.enabled, True)
        self.assertTrue("enabled" in str(c), "cron should be enabled")

        config = dummy_config()
        config.watering_module_activated = False
        db.save_config(config)

        c = cron.CronWithDefault(cron_name="watering_cron", cron_string_default="14h 1,2,3,4,5,6", cron_enabled=True, db=db)
        self.assertEqual(c.cron_string, "23h 1,3,5")
        self.assertEqual(c.enabled, False)
        self.assertTrue("disabled" in str(c), "cron should be enabled")
        self.assertFalse(c.should_it_run(None), False)



    def test_feeding_and_watering(self):
        config = dummy_config()
        config.feeding_module_cronstring = "3h 1,2,3"
        config.feeding_module_activated = False
        config.watering_module_cronstring = "4h 1,2,3"
        config.watering_module_activated = False
        db = database.Database(in_memory=True)
        db.recreate_database()
        db.save_config(config)


        c = cron.FeedingCron(db=db)
        self.assertEqual(c.cron_string, "3h 1,2,3")
        self.assertEqual(c.enabled, False)

        c = cron.WateringCron(db=db)
        self.assertEqual(c.cron_string, "4h 1,2,3")
        self.assertEqual(c.enabled, False)

        db.cursor.execute('DELETE FROM current_config')

        c = cron.WateringCron(db=db)
        self.assertEqual(c.cron_string, constants.WATERING_DEFAULT_CRONSTRING)
        self.assertEqual(c.enabled, True)

        c = cron.FeedingCron(db=db)
        self.assertEqual(c.cron_string, constants.FEEDING_DEFAULT_CRONSTRING)
        self.assertEqual(c.enabled, True)

if __name__ == '__main__':
    unittest.main()
