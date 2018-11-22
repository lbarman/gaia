import sys
import unittest
from datetime import datetime
import os.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
import gaia_server.database as database
import gaia_server.protobufs_pb2 as protobufs_pb2


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


def dummy_status_update():
    status = protobufs_pb2.Status()
    status.authentication_token = "authentication_token_str"
    status.local_timestamp = datetime(2009, 12, 1, 19, 31, 1, 40113).strftime("%Y-%m-%d %H:%M:%S")

    config = status.current_config
    config.feeding_module_activated = True
    config.watering_module_activated = True
    config.feeding_module_cronstring = "12h *"
    config.watering_module_cronstring = "13h 1,3,5"
    config.watering_pump_1_duration = 10
    config.watering_pump_2_duration = 20
    config.watering_pump_3_duration = 30
    config.watering_pump_4_duration = 40

    systemstatus = status.system_status 
    systemstatus.uptime = "uptime_str"
    systemstatus.memory = "memory_str"
    systemstatus.disk_usage = "disk_usage_str"
    systemstatus.processes = "processes_str"
    return status


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

        for expectedTable in ["status", "configs", "system_status", "commands"]:
            if expectedTable not in tables:
                self.fail("Table " + expectedTable + " wasn't created")

    def test_command_creation(self):
        db = database.Database(in_memory=True)
        db.recreate_database()

        # initially, there should be no command
        self.assertEqual(db.get_command(), None)

        db.save_command("SOME_COMMAND")

        # save a command without config
        cmd = db.get_command()
        self.assertNotEqual(cmd, None)
        self.assertEqual(cmd["text"], "SOME_COMMAND")
        self.assertEqual(cmd["config"], None)

        # save a new command, should only keep the most recent
        db.save_command("SOME_COMMAND2")
        cmd = db.get_command()
        self.assertNotEqual(cmd, None)
        self.assertEqual(cmd["text"], "SOME_COMMAND2")
        self.assertEqual(cmd["config"], None)

        self.assertEqual(1, count_records('commands', db.cursor))

        # save a command with config
        config1 = dummy_config()
        db.save_command("SOME_COMMAND3", config1)
        cmd = db.get_command()
        self.assertNotEqual(cmd, None)
        self.assertEqual(cmd["text"], "SOME_COMMAND3")

        config2 = cmd["config"] 
        self.assertEqual(config2['feeding_module_activated'], config1.feeding_module_activated)
        self.assertEqual(config2['watering_module_activated'], config1.watering_module_activated)
        self.assertEqual(config2['feeding_module_cronstring'], config1.feeding_module_cronstring)
        self.assertEqual(config2['watering_module_cronstring'], config1.watering_module_cronstring)
        self.assertEqual(config2['watering_pump_1_duration'], config1.watering_pump_1_duration)
        self.assertEqual(config2['watering_pump_2_duration'], config1.watering_pump_2_duration)
        self.assertEqual(config2['watering_pump_3_duration'], config1.watering_pump_3_duration)
        self.assertEqual(config2['watering_pump_4_duration'], config1.watering_pump_4_duration)

        # saving a new command should overwrite the previous, and hence delete the config

        # save a command with config
        db.save_command("SOME_COMMAND4", None)
        cmd = db.get_command()
        self.assertNotEqual(cmd, None)
        self.assertEqual(cmd["text"], "SOME_COMMAND4")

        self.assertEqual(1, count_records('commands', db.cursor))
        self.assertEqual(0, count_records('configs', db.cursor))

        # delete should empty the table
        db.delete_all_commands()

        self.assertEqual(0, count_records('commands', db.cursor))

    def test_status_creation(self):
        db = database.Database(in_memory=True)
        db.recreate_database()

        # initially, there should be no command
        self.assertEqual(db.get_all_status(), [])

        # save and retrieve one
        status1 = dummy_status_update()

        db.save_status(status1)
        all_status = db.get_all_status()
        self.assertNotEqual(all_status, None)
        self.assertEqual(len(all_status), 1)
        status2 = all_status[0]

        self.assertEqual(status2['local_timestamp'].strftime("%Y-%m-%d %H:%M:%S"), status1.local_timestamp)
        self.assertEqual(status2['feeding_module_activated'], status1.current_config.feeding_module_activated)
        self.assertEqual(status2['watering_module_activated'], status1.current_config.watering_module_activated)
        self.assertEqual(status2['feeding_module_cronstring'], status1.current_config.feeding_module_cronstring)
        self.assertEqual(status2['watering_module_cronstring'], status1.current_config.watering_module_cronstring)
        self.assertEqual(status2['watering_pump_1_duration'], status1.current_config.watering_pump_1_duration)
        self.assertEqual(status2['watering_pump_2_duration'], status1.current_config.watering_pump_2_duration)
        self.assertEqual(status2['watering_pump_3_duration'], status1.current_config.watering_pump_3_duration)
        self.assertEqual(status2['watering_pump_4_duration'], status1.current_config.watering_pump_4_duration)
        self.assertEqual(status2['uptime'], status1.system_status.uptime)
        self.assertEqual(status2['memory'], status1.system_status.memory)
        self.assertEqual(status2['disk_usage'], status1.system_status.disk_usage)
        self.assertEqual(status2['processes'], status1.system_status.processes)

        self.assertEqual(1, count_records('configs', db.cursor))
        self.assertEqual(1, count_records('system_status', db.cursor))
        self.assertEqual(1, count_records('status', db.cursor))

        db.save_status(status1)
        self.assertEqual(2, count_records('configs', db.cursor))
        self.assertEqual(2, count_records('system_status', db.cursor))
        self.assertEqual(2, count_records('status', db.cursor))

        # should remove all things older than X days, here with X=0 => table should be truncated
        db.save_status(status1, number_of_days_to_keep_status=0)
        self.assertEqual(1, count_records('configs', db.cursor))
        self.assertEqual(1, count_records('system_status', db.cursor))
        self.assertEqual(1, count_records('status', db.cursor))


if __name__ == '__main__':
    unittest.main()
