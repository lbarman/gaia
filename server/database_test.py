import unittest

from database import *
import protobufs_pb2

def dummyConfig():
    config = protobufs_pb2.Config()
    config.feeding_module_activated = True;
    config.watering_module_activated = True;
    config.feeding_module_cronstring = "12 *";
    config.watering_module_cronstring = "13 1,3,5";
    config.watering_pump_1_duration = 10;
    config.watering_pump_2_duration = 20;
    config.watering_pump_3_duration = 30;
    config.watering_pump_4_duration = 40;
    return config

def dummyStatusUpdate():
    status = protobufs_pb2.Status()
    status.authentication_token = "authentication_token_str";
    status.local_timestamp = datetime(2009, 12, 1, 19, 31, 1, 40113).strftime("%Y-%m-%d %H:%M:%S")

    config = status.current_config
    config.feeding_module_activated = True;
    config.watering_module_activated = True;
    config.feeding_module_cronstring = "12 *";
    config.watering_module_cronstring = "13 1,3,5";
    config.watering_pump_1_duration = 10;
    config.watering_pump_2_duration = 20;
    config.watering_pump_3_duration = 30;
    config.watering_pump_4_duration = 40;

    systemstatus = status.system_status 
    systemstatus.uptime = "uptime_str";
    systemstatus.memory = "memory_str";
    systemstatus.disk_usage = "disk_usage_str";
    systemstatus.processes = "processes_str";
    return status

class DatabaseTest(unittest.TestCase):

    def test_db_creation(self):
        db = Database(inMemory=True)
        self.assertNotEqual(db.db, None)
        self.assertNotEqual(db.cursor, None)

        db.recreateDatabase()

        self.assertNotEqual(db.db, None)
        self.assertNotEqual(db.cursor, None)

        tables = db.cursor.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
        tables = [x[0] for x in tables]

        for expectedTable in ["status", "configs", "system_status", "commands"]:
            if expectedTable not in tables:
                self.fail("Table", expectedTable, "wasn't created")

    def test_command_creation(self):
        db = Database(inMemory=True)
        db.recreateDatabase()

        # initially, there should be no command
        self.assertEqual(db.getCommand(), None)

        db.saveCommand("SOME_COMMAND")

        # save a command without config
        cmd = db.getCommand()
        self.assertNotEqual(cmd, None)
        self.assertEqual(cmd["text"], "SOME_COMMAND")
        self.assertEqual(cmd["config"], None)

        # save a new command, should only keep the most recent
        db.saveCommand("SOME_COMMAND2")
        cmd = db.getCommand()
        self.assertNotEqual(cmd, None)
        self.assertEqual(cmd["text"], "SOME_COMMAND2")
        self.assertEqual(cmd["config"], None)

        count = db.cursor.execute("SELECT count(*) FROM commands").fetchone()[0]
        self.assertEqual(count, 1)

        # save a command with config
        config1 = dummyConfig()
        db.saveCommand("SOME_COMMAND3", config1)
        cmd = db.getCommand()
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
        db.saveCommand("SOME_COMMAND4", None)
        cmd = db.getCommand()
        self.assertNotEqual(cmd, None)
        self.assertEqual(cmd["text"], "SOME_COMMAND4")

        count = db.cursor.execute("SELECT count(*) FROM commands").fetchone()[0]
        self.assertEqual(count, 1)

        count = db.cursor.execute("SELECT count(*) FROM configs").fetchone()[0]
        self.assertEqual(count, 0)

        # delete should empty the table
        db.deleteAllCommands()

        count = db.cursor.execute("SELECT count(*) FROM commands").fetchone()[0]
        self.assertEqual(count, 0)

    def test_status_creation(self):
        db = Database(inMemory=True)
        db.recreateDatabase()

        # initially, there should be no command
        self.assertEqual(db.getAllStatus(), [])

        # save and retrieve one
        status1 = dummyStatusUpdate()

        db.saveStatus(status1)
        allStatus = db.getAllStatus()
        self.assertNotEqual(allStatus, None)
        self.assertEqual(len(allStatus), 1)
        status2 = allStatus[0]

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

        self.assertEqual(1, db.cursor.execute("SELECT count(*) FROM configs").fetchone()[0])
        self.assertEqual(1, db.cursor.execute("SELECT count(*) FROM system_status").fetchone()[0])
        self.assertEqual(1, db.cursor.execute("SELECT count(*) FROM status").fetchone()[0])

        db.saveStatus(status1)
        self.assertEqual(2, db.cursor.execute("SELECT count(*) FROM configs").fetchone()[0])
        self.assertEqual(2, db.cursor.execute("SELECT count(*) FROM system_status").fetchone()[0])
        self.assertEqual(2, db.cursor.execute("SELECT count(*) FROM status").fetchone()[0])

        # should remove all things older than X days, here with X=0 => table should be truncated
        db.saveStatus(status1, numberOfDaysToKeepStatus=0)
        self.assertEqual(1, db.cursor.execute("SELECT count(*) FROM configs").fetchone()[0])
        self.assertEqual(1, db.cursor.execute("SELECT count(*) FROM system_status").fetchone()[0])
        self.assertEqual(1, db.cursor.execute("SELECT count(*) FROM status").fetchone()[0])

if __name__ == '__main__':
    unittest.main()