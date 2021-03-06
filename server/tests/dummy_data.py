import sys
from datetime import datetime, timedelta
import os.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
import gaia_server.database as database
import gaia_server.protobufs_pb2 as protobufs_pb2


def dummy_status_update(day, hour, min):

    index = day + 24 * hour + 60 * min

    status = protobufs_pb2.Status()
    status_date = datetime.today() - timedelta(days=day, hours=hour, minutes=10*min)

    status.authentication_token = "authentication_token_str"
    status.local_timestamp = status_date.strftime("%Y-%m-%d %H:%M:%S")
    status.temperature = (10 + index) % 20 + 10
    status.humidity = (20 + index) % 20 + 10
    status.temperature2 = (15.1 + index) % 20 + 10
    status.temperature3 = (25.2 + index) % 20 + 10

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

def dummy_action_report(day):
    report_date = datetime.today() - timedelta(days=day)

    action_report = protobufs_pb2.ActionReport()
    action_report.local_timestamp = report_date.strftime("%Y-%m-%d %H:%M:%S")

    if day % 2 == 0:
        action_report.action = protobufs_pb2.ActionReport.FEEDING
    else:
        action_report.action = protobufs_pb2.ActionReport.WATERING

    action_report.action_details = "a long string for day " + str(day)
    return action_report

    return status


def insert_dummy_pings():
    db = database.Database()
    db.recreate_database()

    for day in range(0,7):
        for hour in range(0,24):
            for min in range(0,6):
                db.save_status(dummy_status_update(day, hour, min))

def insert_dummy_action_report():
    db = database.Database()
    db.recreate_database()

    for i in range(0,14):
        db.save_action_report(dummy_action_report(i))


if __name__ == '__main__':
    insert_dummy_pings()
    insert_dummy_action_report()
