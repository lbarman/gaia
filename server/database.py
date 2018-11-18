from constants import *

import sqlite3
from datetime import datetime, timedelta

class Database:

    db = None
    cursor = None

    def __init__(self):
        self.db = sqlite3.connect(SQLITE_DATABASE_PATH, detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
        self.cursor = self.db.cursor()
        self.cursor.execute('PRAGMA foreign_keys=ON;')

    def recreateDatabase(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS status (
              `id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
              `server_timestamp` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
              `local_timestamp` DATETIME DEFAULT NULL
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS commands (
            `id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            `server_timestamp` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            `text` TEXT
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS configs (
              `id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
              `status_id` INTEGER,
              `command_id` INTEGER,
              `feeding_module_activated` BOOLEAN DEFAULT False,
              `watering_module_activated` BOOLEAN DEFAULT False,
              `feeding_module_cronstring` VARCHAR(50) DEFAULT "",
              `watering_module_cronstring` VARCHAR(50) DEFAULT "",
              `watering_pump_1_duration` INTEGER DEFAULT 0,
              `watering_pump_2_duration` INTEGER DEFAULT 0,
              `watering_pump_3_duration` INTEGER DEFAULT 0,
              `watering_pump_4_duration` INTEGER DEFAULT 0,
               FOREIGN KEY(status_id) REFERENCES status(id) ON DELETE CASCADE,
               FOREIGN KEY(command_id) REFERENCES commands(id) ON DELETE CASCADE
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS system_status(
            `id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            `status_id` INTEGER NOT NULL,
            `uptime` TEXT,
            `memory` TEXT,
            `disk_usage` TEXT,
            `processes` TEXT,
            FOREIGN KEY(status_id) REFERENCES status(id) ON DELETE CASCADE
            )
        ''')
        self.db.commit()

    def saveCommand(self, text, config=None):
        self.cursor.execute('''DELETE FROM commands''')
        self.cursor.execute('''INSERT INTO commands(text) VALUES (?)''', (text,))

        if config != None:
            command_id = self.cursor.execute('SELECT last_insert_rowid()').fetchone()[0]

            self.cursor.execute('''INSERT INTO configs(
            command_id,
            feeding_module_activated,
            watering_module_activated,
            feeding_module_cronstring,
            watering_module_cronstring,
            watering_pump_1_duration,
            watering_pump_2_duration,
            watering_pump_3_duration,
            watering_pump_4_duration) VALUES (?,?,?,?,?,?,?,?,?)''',
            (command_id,
            config.feeding_module_activated,
            config.watering_module_activated,
            config.feeding_module_cronstring,
            config.watering_module_cronstring,
            config.watering_pump_1_duration,
            config.watering_pump_2_duration,
            config.watering_pump_3_duration,
            config.watering_pump_4_duration))

        self.db.commit()

    def getCommand(self):
        self.cursor.execute('''SELECT id, server_timestamp, text FROM commands ORDER BY id DESC''')
        answer = {}
        row = self.cursor.fetchone()
        answer['id'] = row[0]
        answer['server_timestamp'] = datetime.strptime(row[1], "%Y-%m-%d %H:%M:%S")
        answer['text'] = row[2]
        return answer

    def saveStatus(self, protobufStatus):
        
        # delete things older than 1 week ago
        oneWeekAgo = datetime.today() - timedelta(days=NUMBER_OF_DAYS_TO_KEEP_STATUS)
        oneWeekAgoStr = oneWeekAgo.strftime("%Y-%m-%d %H:%M:%S")
        self.cursor.execute('''DELETE FROM status WHERE (?)''', (oneWeekAgoStr,))

        # insert new
        self.cursor.execute('''INSERT INTO status(local_timestamp) VALUES (?)''',
            (protobufStatus.local_timestamp,))
        status_id = self.cursor.execute('SELECT last_insert_rowid()').fetchone()[0]

        config = protobufStatus.current_config;
        self.cursor.execute('''INSERT INTO configs(
            status_id,
            feeding_module_activated,
            watering_module_activated,
            feeding_module_cronstring,
            watering_module_cronstring,
            watering_pump_1_duration,
            watering_pump_2_duration,
            watering_pump_3_duration,
            watering_pump_4_duration) VALUES (?,?,?,?,?,?,?,?,?)''',
            (status_id,
            config.feeding_module_activated,
            config.watering_module_activated,
            config.feeding_module_cronstring,
            config.watering_module_cronstring,
            config.watering_pump_1_duration,
            config.watering_pump_2_duration,
            config.watering_pump_3_duration,
            config.watering_pump_4_duration))

        system_status = protobufStatus.system_status;
        self.cursor.execute('''INSERT INTO system_status(
            status_id,
            uptime,
            memory,
            disk_usage,
            processes) VALUES (?,?,?,?,?)''',
            (status_id,
            system_status.uptime,
            system_status.memory,
            system_status.disk_usage,
            system_status.processes))

        self.db.commit()

    def getAllStatus(self):
        self.cursor.execute('''SELECT 
            status.id,
            status.local_timestamp,
            configs.feeding_module_activated,
            configs.watering_module_activated,
            configs.feeding_module_cronstring,
            configs.watering_module_cronstring,
            configs.watering_pump_1_duration,
            configs.watering_pump_2_duration,
            configs.watering_pump_3_duration,
            configs.watering_pump_4_duration,
            system_status.uptime,
            system_status.memory,
            system_status.disk_usage,
            system_status.processes
            FROM status 
            LEFT JOIN configs ON status.id == configs.status_id
            LEFT JOIN system_status ON status.id == system_status.status_id
            ORDER BY status.id DESC''')

        answer = []
        for row in self.cursor:
            typedRow = {}
            typedRow['id'] = row[0]
            typedRow['local_timestamp'] = datetime.strptime(row[1], "%Y-%m-%d %H:%M:%S")
            typedRow['feeding_module_activated'] = row[2]
            typedRow['watering_module_activated'] = row[3]
            typedRow['feeding_module_cronstring'] = row[4]
            typedRow['watering_module_cronstring'] = row[5]
            typedRow['watering_pump_1_duration'] = row[6]
            typedRow['watering_pump_2_duration'] = row[7]
            typedRow['watering_pump_3_duration'] = row[8]
            typedRow['watering_pump_4_duration'] = row[9]
            typedRow['uptime'] = row[10]
            typedRow['memory'] = row[11]
            typedRow['disk_usage'] = row[12]
            typedRow['processes'] = row[12]
            answer.append(typedRow)

        return answer