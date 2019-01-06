import sys
import os.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
import unittest
import grpc
from datetime import datetime
import gaia_server.protobufs_pb2 as protobufs_pb2
import gaia_server.protobufs_pb2_grpc as protobufs_pb2_grpc

def dummy_status_message():
    status = protobufs_pb2.Status()
    status.authentication_token = "authentication_token_str"
    status.local_timestamp = datetime(2009, 12, 1, 19, 31, 1, 40113).strftime("%Y-%m-%d %H:%M:%S")
    status.temperature = 12
    status.humidity = 13
    status.temperature2 = 24.1
    status.temperature3 = 25.2

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

# create the gRPC stub
channel = grpc.insecure_channel('127.0.0.1:8015')
stub = protobufs_pb2_grpc.GaiaServiceStub(channel)

# send message
response = stub.Ping(dummy_status_message())
print(response)
