import sqlite3
import gaia_client.constants as constants
from datetime import datetime

class Database:
    db = None
    cursor = None

    def __init__(self, in_memory=False, database_path=constants.SQLITE_DATABASE_PATH):
        if in_memory:
            database_path = ":memory:"

        self.db = sqlite3.connect(database_path)
        self.cursor = self.db.cursor()
        self.cursor.execute('PRAGMA foreign_keys=ON;')

    def recreate_database(self):
        self.cursor.execute('\n'
                            '            CREATE TABLE IF NOT EXISTS cron (\n'
                            '              `name` VARCHAR(50)   NOT NULL,\n'
                            '              `cron_string` VARCHAR(50)   NOT NULL,\n'
                            '              `last_run` DATETIME\n'
                            '            )\n'
                            '        ')
        self.cursor.execute('\n'
                            '            CREATE TABLE IF NOT EXISTS current_config (\n'
                            '              `id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,\n'
                            '              `updated` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,\n'
                            '              `feeding_module_activated` BOOLEAN DEFAULT False,\n'
                            '              `watering_module_activated` BOOLEAN DEFAULT False,\n'
                            '              `feeding_module_cronstring` VARCHAR(50) DEFAULT "",\n'
                            '              `watering_module_cronstring` VARCHAR(50) DEFAULT "",\n'
                            '              `watering_pump_1_duration` INTEGER DEFAULT 0,\n'
                            '              `watering_pump_2_duration` INTEGER DEFAULT 0,\n'
                            '              `watering_pump_3_duration` INTEGER DEFAULT 0,\n'
                            '              `watering_pump_4_duration` INTEGER DEFAULT 0\n'
                            '            )\n'
                            '        ')
        self.db.commit()

    def delete_all_cron(self):
        self.cursor.execute('DELETE FROM cron')
        self.db.commit()

    def save_cron(self, name, cron_string, last_run):
        self.cursor.execute('SELECT count(*) FROM cron WHERE name=(?)', (name,))
        count = self.cursor.fetchone()


        if count[0] == 0:
            self.cursor.execute('INSERT INTO cron(name, cron_string, last_run) VALUES (?,?,?)',
                                (name, cron_string, constants.CRON_TIME0))

        self.cursor.execute('UPDATE cron SET cron_string=?, last_run=? WHERE name=?',
                            (cron_string, last_run.replace(microsecond=0), name))

        self.db.commit()


    def get_all_cron(self, name_filter=None):
        if name_filter is None:
            self.cursor.execute('SELECT name, cron_string, last_run FROM cron')
        else:
            self.cursor.execute('SELECT name, cron_string, last_run FROM cron WHERE name=?', (name_filter,))

        rows = self.cursor.fetchall()

        res = dict()

        for row in rows:
            name = row[0]
            res[name] = dict()
            res[name]['cron_string'] = row[1]
            res[name]['last_run'] = datetime.strptime(row[2], "%Y-%m-%d %H:%M:%S")

        return res

    def get_cron_perhaps_create(self, name):
        self.cursor.execute('SELECT count(*) FROM cron WHERE name=(?)', (name,))
        count = self.cursor.fetchone()

        if count[0] == 0:
            self.cursor.execute('INSERT INTO cron(name, cron_string, last_run) VALUES (?,?,?)',
                                (name, '?', constants.CRON_TIME0))


        self.cursor.execute('SELECT cron_string, last_run FROM cron WHERE name=?', (name,))
        row = self.cursor.fetchone()

        cron = dict()
        cron['cron_string'] = row[0]
        cron['last_run'] = datetime.strptime(row[1], "%Y-%m-%d %H:%M:%S")
        return cron


    def save_config(self, config):

        self.cursor.execute('DELETE FROM current_config')
        self.cursor.execute('INSERT INTO current_config(\n'
                            '            feeding_module_activated,\n'
                            '            watering_module_activated,\n'
                            '            feeding_module_cronstring,\n'
                            '            watering_module_cronstring,\n'
                            '            watering_pump_1_duration,\n'
                            '            watering_pump_2_duration,\n'
                            '            watering_pump_3_duration,\n'
                            '            watering_pump_4_duration) VALUES (?,?,?,?,?,?,?,?)',
                            (config.feeding_module_activated,
                             config.watering_module_activated,
                             config.feeding_module_cronstring,
                             config.watering_module_cronstring,
                             config.watering_pump_1_duration,
                             config.watering_pump_2_duration,
                             config.watering_pump_3_duration,
                             config.watering_pump_4_duration))
        self.db.commit()

    def get_config(self):
        self.cursor.execute('SELECT \n'
                            '            id,\n'
                            '            updated,\n'
                            '            feeding_module_activated,\n'
                            '            watering_module_activated,\n'
                            '            feeding_module_cronstring,\n'
                            '            watering_module_cronstring,\n'
                            '            watering_pump_1_duration,\n'
                            '            watering_pump_2_duration,\n'
                            '            watering_pump_3_duration,\n'
                            '            watering_pump_4_duration\n'
                            '            FROM current_config ORDER BY id DESC LIMIT 1')

        row = self.cursor.fetchone()

        if row is None:
            return None

        config = dict()
        config['id'] = row[0]
        config['updated'] = datetime.strptime(row[1], "%Y-%m-%d %H:%M:%S")
        config['feeding_module_activated'] = row[2]
        config['watering_module_activated'] = row[3]
        config['feeding_module_cronstring'] = row[4]
        config['watering_module_cronstring'] = row[5]
        config['watering_pump_1_duration'] = row[6]
        config['watering_pump_2_duration'] = row[7]
        config['watering_pump_3_duration'] = row[8]
        config['watering_pump_4_duration'] = row[9]

        return config

    def reset_db(self):
        self.cursor.execute('DROP TABLE cron;')
        self.cursor.execute('DROP TABLE current_config;')
        self.db.commit()
        self.recreate_database()
