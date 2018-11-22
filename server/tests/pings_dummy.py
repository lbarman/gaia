import sys
import unittest
from datetime import datetime
import os.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
import gaia_server.database as database
import gaia_server.protobufs_pb2 as protobufs_pb2


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

def insert_dummy_pings():
    db = database.Database()
    db.recreate_database()

