from constants import *

import sqlite3
from datetime import datetime, timedelta


class Database:
    db = None
    cursor = None

    def __init__(self, in_memory=False, database_path=SQLITE_DATABASE_PATH):
        if in_memory:
            database_path = ":memory:"

        self.db = sqlite3.connect(database_path)
        self.cursor = self.db.cursor()
        self.cursor.execute('PRAGMA foreign_keys=ON;')

    def recreate_database(self):
        self.cursor.execute('\n'
                            '            CREATE TABLE IF NOT EXISTS status (\n'
                            '              `id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,\n'
                            '              `server_timestamp` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,\n'
                            '              `local_timestamp` DATETIME DEFAULT NULL\n'
                            '            )\n'
                            '        ')
        self.cursor.execute('\n'
                            '            CREATE TABLE IF NOT EXISTS commands (\n'
                            '            `id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,\n'
                            '            `server_timestamp` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,\n'
                            '            `text` TEXT\n'
                            '            )\n'
                            '        ')
        self.cursor.execute('\n'
                            '            CREATE TABLE IF NOT EXISTS configs (\n'
                            '              `id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,\n'
                            '              `status_id` INTEGER,\n'
                            '              `command_id` INTEGER,\n'
                            '              `feeding_module_activated` BOOLEAN DEFAULT False,\n'
                            '              `watering_module_activated` BOOLEAN DEFAULT False,\n'
                            '              `feeding_module_cronstring` VARCHAR(50) DEFAULT "",\n'
                            '              `watering_module_cronstring` VARCHAR(50) DEFAULT "",\n'
                            '              `watering_pump_1_duration` INTEGER DEFAULT 0,\n'
                            '              `watering_pump_2_duration` INTEGER DEFAULT 0,\n'
                            '              `watering_pump_3_duration` INTEGER DEFAULT 0,\n'
                            '              `watering_pump_4_duration` INTEGER DEFAULT 0,\n'
                            '               FOREIGN KEY(status_id) REFERENCES status(id) ON DELETE CASCADE,\n'
                            '               FOREIGN KEY(command_id) REFERENCES commands(id) ON DELETE CASCADE\n'
                            '            )\n'
                            '        ')
        self.cursor.execute('\n'
                            '            CREATE TABLE IF NOT EXISTS system_status(\n'
                            '            `id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,\n'
                            '            `status_id` INTEGER NOT NULL,\n'
                            '            `uptime` TEXT,\n'
                            '            `memory` TEXT,\n'
                            '            `disk_usage` TEXT,\n'
                            '            `processes` TEXT,\n'
                            '            FOREIGN KEY(status_id) REFERENCES status(id) ON DELETE CASCADE\n'
                            '            )\n'
                            '        ')
        self.db.commit()

    def delete_all_commands(self):
        self.cursor.execute('DELETE FROM commands')
        self.db.commit()

    def save_command(self, text, config=None):
        self.cursor.execute('DELETE FROM commands')
        self.cursor.execute('INSERT INTO commands(text) VALUES (?)', (text,))

        if config is not None:
            command_id = self.cursor.execute('SELECT last_insert_rowid()').fetchone()[0]

            self.cursor.execute('INSERT INTO configs(\n'
                                '            command_id,\n'
                                '            feeding_module_activated,\n'
                                '            watering_module_activated,\n'
                                '            feeding_module_cronstring,\n'
                                '            watering_module_cronstring,\n'
                                '            "watering_pump_1_duration",\n'
                                '            watering_pump_2_duration,\n'
                                '            watering_pump_3_duration,\n'
                                '            watering_pump_4_duration) VALUES (?,?,?,?,?,?,?,?,?)',
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

    def get_command(self):
        self.cursor.execute('SELECT \n'
                            '            commands.id,\n'
                            '            commands.server_timestamp,\n'
                            '            commands.text,\n'
                            '            configs.feeding_module_activated,\n'
                            '            configs.watering_module_activated,\n'
                            '            configs.feeding_module_cronstring,\n'
                            '            configs.watering_module_cronstring,\n'
                            '            configs.watering_pump_1_duration,\n'
                            '            configs.watering_pump_2_duration,\n'
                            '            configs.watering_pump_3_duration,\n'
                            '            configs.watering_pump_4_duration\n'
                            '            FROM commands \n'
                            '            LEFT JOIN configs ON commands.id == configs.command_id\n'
                            '            ORDER BY commands.id DESC')

        answer = {}
        row = self.cursor.fetchone()

        if row is None:
            return None

        answer['id'] = row[0]
        answer['server_timestamp'] = datetime.strptime(row[1], "%Y-%m-%d %H:%M:%S")
        answer['text'] = row[2]
        config = None

        if row[3] is not None and row[4] is not None:
            config = dict()
            config['feeding_module_activated'] = row[3]
            config['watering_module_activated'] = row[4]
            config['feeding_module_cronstring'] = row[5]
            config['watering_module_cronstring'] = row[6]
            config['watering_pump_1_duration'] = row[7]
            config['watering_pump_2_duration'] = row[8]
            config['watering_pump_3_duration'] = row[9]
            config['watering_pump_4_duration'] = row[10]

        answer['config'] = config

        return answer

    def save_status(self, status_pb2, number_of_days_to_keep_status=NUMBER_OF_DAYS_TO_KEEP_STATUS):

        # delete things older than 1 week ago
        one_week_ago = datetime.today() - timedelta(days=number_of_days_to_keep_status)
        one_week_ago_str = one_week_ago.strftime("%Y-%m-%d %H:%M:%S")
        self.cursor.execute('DELETE FROM status WHERE server_timestamp <= (?)', (one_week_ago_str,))

        # insert new
        self.cursor.execute('INSERT INTO status(local_timestamp) VALUES (?)',
                            (status_pb2.local_timestamp,))
        status_id = self.cursor.execute('SELECT last_insert_rowid()').fetchone()[0]

        config = status_pb2.current_config
        self.cursor.execute('INSERT INTO configs(\n'
                            '            status_id,\n'
                            '            feeding_module_activated,\n'
                            '            watering_module_activated,\n'
                            '            feeding_module_cronstring,\n'
                            '            watering_module_cronstring,\n'
                            '            watering_pump_1_duration,\n'
                            '            watering_pump_2_duration,\n'
                            '            watering_pump_3_duration,\n'
                            '            watering_pump_4_duration) VALUES (?,?,?,?,?,?,?,?,?)',
                            (status_id,
                             config.feeding_module_activated,
                             config.watering_module_activated,
                             config.feeding_module_cronstring,
                             config.watering_module_cronstring,
                             config.watering_pump_1_duration,
                             config.watering_pump_2_duration,
                             config.watering_pump_3_duration,
                             config.watering_pump_4_duration))

        system_status = status_pb2.system_status
        self.cursor.execute('INSERT INTO system_status(\n'
                            '            status_id,\n'
                            '            uptime,\n'
                            '            memory,\n'
                            '            disk_usage,\n'
                            '            processes) VALUES (?,?,?,?,?)',
                            (status_id,
                             system_status.uptime,
                             system_status.memory,
                             system_status.disk_usage,
                             system_status.processes))

        self.db.commit()

    def get_all_status(self):
        self.cursor.execute('SELECT \n'
                            '            status.id,\n'
                            '            status.local_timestamp,\n'
                            '            configs.feeding_module_activated,\n'
                            '            configs.watering_module_activated,\n'
                            '            configs.feeding_module_cronstring,\n'
                            '            configs.watering_module_cronstring,\n'
                            '            configs.watering_pump_1_duration,\n'
                            '            configs.watering_pump_2_duration,\n'
                            '            configs.watering_pump_3_duration,\n'
                            '            configs.watering_pump_4_duration,\n'
                            '            system_status.uptime,\n'
                            '            system_status.memory,\n'
                            '            system_status.disk_usage,\n'
                            '            system_status.processes\n'
                            '            FROM status \n'
                            '            LEFT JOIN configs ON status.id == configs.status_id\n'
                            '            LEFT JOIN system_status ON status.id == system_status.status_id\n'
                            '            ORDER BY status.id DESC')

        answer = []
        for row in self.cursor:
            named_row = dict()
            named_row['id'] = row[0]
            named_row['local_timestamp'] = datetime.strptime(row[1], "%Y-%m-%d %H:%M:%S")
            named_row['feeding_module_activated'] = row[2]
            named_row['watering_module_activated'] = row[3]
            named_row['feeding_module_cronstring'] = row[4]
            named_row['watering_module_cronstring'] = row[5]
            named_row['watering_pump_1_duration'] = row[6]
            named_row['watering_pump_2_duration'] = row[7]
            named_row['watering_pump_3_duration'] = row[8]
            named_row['watering_pump_4_duration'] = row[9]
            named_row['uptime'] = row[10]
            named_row['memory'] = row[11]
            named_row['disk_usage'] = row[12]
            named_row['processes'] = row[13]
            answer.append(named_row)

        return answer
