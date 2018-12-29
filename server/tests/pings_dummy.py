import sys
import unittest
from datetime import datetime, timedelta
import os.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
import gaia_server.database as database
import gaia_server.protobufs_pb2 as protobufs_pb2


def dummy_status_update(index):
    status = protobufs_pb2.Status()
    status_date = datetime.today() - timedelta(days=index)

    status.authentication_token = "authentication_token_str"
    status.local_timestamp = status_date.strftime("%Y-%m-%d %H:%M:%S")
    status.temperature = (10 + index) % 20 + 10
    status.humidity = (20 + index) % 20 + 10
    status.temperature2 = (10.1 + index) % 20 + 10
    status.temperature3 = (20.2 + index) % 20 + 10

    config = status.current_config
    config.feeding_module_activated = (index % 2 == 0)
    config.watering_module_activated = (index % 2 == 1)
    config.feeding_module_cronstring = str(index % 24) + "h *"
    config.watering_module_cronstring = str(index % 24) + "h 1,3,5"
    config.watering_pump_1_duration = 10 + index
    config.watering_pump_2_duration = 20 + index
    config.watering_pump_3_duration = 30 + index
    config.watering_pump_4_duration = 40 + index

    systemstatus = status.system_status
    systemstatus.uptime = "uptime_str" + str(index)
    systemstatus.memory = "memory_str" + str(index)
    systemstatus.disk_usage = "disk_usage_str" + str(index)
    systemstatus.processes = "processes_str" + str(index)
    return status


def insert_dummy_pings():
    db = database.Database()
    db.recreate_database()

    for i in range(0, 40):
        db.save_status(dummy_status_update(i))


if __name__ == '__main__':
    insert_dummy_pings()
