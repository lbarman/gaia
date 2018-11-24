import sys
import unittest
from datetime import datetime
import os.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
import gaia_client.database as database
import gaia_client.protobufs_pb2 as protobufs_pb2

def dummy_config():
    config = protobufs_pb2.Config()
    config.feeding_module_activated = True
    config.watering_module_activated = True
    config.feeding_module_cronstring = "12h *"
    config.watering_module_cronstring = "13h 1,3,5"
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


class DatabaseTest(unittest.TestCase):

    def test_db_creation(self):
        db = database.Database(in_memory=True)
        self.assertNotEqual(db.db, None)
        self.assertNotEqual(db.cursor, None)

        db.recreate_database()

        self.assertNotEqual(db.db, None)
        self.assertNotEqual(db.cursor, None)

        tables = db.cursor.execute('SELECT name FROM sqlite_master WHERE type=\'table\'').fetchall()
        tables = [x[0] for x in tables]

        for expectedTable in ["current_config", "cron"]:
            if expectedTable not in tables:
                self.fail("Table " + expectedTable + " wasn't created")

    def test_cron(self):
        db = database.Database(in_memory=True)
        db.recreate_database()

        self.assertEqual(count_records('cron', db.cursor), 0)
        self.assertDictEqual(db.get_all_cron(), dict())

        # insert one
        cron_name = 'test'
        cron_str = '12h *'
        now = datetime.now().replace(microsecond=0)
        db.save_cron(cron_name, cron_str, now)

        # assert it's in there
        self.assertEqual(count_records('cron', db.cursor), 1)
        all_crons = db.get_all_cron()
        expected = dict()
        expected[cron_name] = dict()
        expected[cron_name]['cron_string'] = cron_str
        expected[cron_name]['last_run'] = now
        self.assertDictEqual(all_crons, expected)


        # update one
        cron_str = '15h *'
        now = datetime.now().replace(microsecond=0)
        db.save_cron(cron_name, cron_str, now)

        # assert it's in there
        self.assertEqual(count_records('cron', db.cursor), 1)
        all_crons = db.get_all_cron()
        expected = dict()
        expected[cron_name] = dict()
        expected[cron_name]['cron_string'] = cron_str
        expected[cron_name]['last_run'] = now
        self.assertDictEqual(all_crons, expected)

        # empty the db
        db.delete_all_cron()
        self.assertEqual(count_records('cron', db.cursor), 0)
        self.assertDictEqual(db.get_all_cron(), dict())

        # insert one
        cron_name = 'test'
        cron_str = '12h *'
        now = datetime.now().replace(microsecond=0)
        db.save_cron(cron_name, cron_str, now)

        # assert it's in there
        self.assertEqual(count_records('cron', db.cursor), 1)
        all_crons = db.get_all_cron()
        expected = dict()
        expected[cron_name] = dict()
        expected[cron_name]['cron_string'] = cron_str
        expected[cron_name]['last_run'] = now
        self.assertDictEqual(all_crons, expected)

        # insert another
        cron_name = 'test2'
        cron_str = '02h 1,4,6'
        now = datetime.now().replace(microsecond=0)
        db.save_cron(cron_name, cron_str, now)

        # assert it's in there
        self.assertEqual(count_records('cron', db.cursor), 2)
        all_crons = db.get_all_cron()

        expected[cron_name] = dict()
        expected[cron_name]['cron_string'] = cron_str
        expected[cron_name]['last_run'] = now
        self.assertDictEqual(all_crons, expected)

        # update them individually
        now = datetime.now().replace(microsecond=0)
        db.save_cron(cron_name, cron_str, now)

        # assert it's in there
        self.assertEqual(count_records('cron', db.cursor), 2)
        all_crons = db.get_all_cron()

        expected[cron_name]['cron_string'] = cron_str
        expected[cron_name]['last_run'] = now
        self.assertDictEqual(all_crons, expected)

        # update them individually
        cron_name = 'test'
        now = datetime.now().replace(microsecond=0)
        db.save_cron(cron_name, cron_str, now)

        # assert it's in there
        self.assertEqual(count_records('cron', db.cursor), 2)
        all_crons = db.get_all_cron()

        expected[cron_name]['cron_string'] = cron_str
        expected[cron_name]['last_run'] = now
        self.assertDictEqual(all_crons, expected)


        single_dict = dict()
        single_dict[cron_name] = dict()
        single_dict[cron_name]['cron_string'] = cron_str
        single_dict[cron_name]['last_run'] = now
        self.assertDictEqual(db.get_all_cron(cron_name), single_dict)

    def test_config(self):
        db = database.Database(in_memory=True)
        db.recreate_database()

        self.assertEqual(count_records('current_config', db.cursor), 0)
        self.assertEqual(db.get_config(), None)

        config = dummy_config()
        db.save_config(config)

        self.assertEqual(count_records('current_config', db.cursor), 1)
        self.assertNotEqual(db.get_config(), None)

        # only saves the latest
        db.save_config(config)

        self.assertEqual(count_records('current_config', db.cursor), 1)
        self.assertNotEqual(db.get_config(), None)

        config2 = db.get_config()
        self.assertEqual(config2['id'], 2)
        self.assertTrue(isinstance(config2['updated'], datetime))
        self.assertEqual(config2['feeding_module_activated'], config.feeding_module_activated)
        self.assertEqual(config2['watering_module_activated'], config.watering_module_activated)
        self.assertEqual(config2['feeding_module_cronstring'], config.feeding_module_cronstring)
        self.assertEqual(config2['watering_module_cronstring'], config.watering_module_cronstring)
        self.assertEqual(config2['watering_pump_1_duration'], config.watering_pump_1_duration)
        self.assertEqual(config2['watering_pump_2_duration'], config.watering_pump_2_duration)
        self.assertEqual(config2['watering_pump_3_duration'], config.watering_pump_3_duration)
        self.assertEqual(config2['watering_pump_4_duration'], config.watering_pump_4_duration)



if __name__ == '__main__':
    unittest.main()
