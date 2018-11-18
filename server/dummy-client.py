from concurrent import futures
import time
import math

import grpc

import protobufs_pb2
import protobufs_pb2_grpc

channel = grpc.insecure_channel('127.0.0.1:50051')
stub = protobufs_pb2_grpc.GaiaServiceStub(channel)

print("Doing request")

status = protobufs_pb2.Status()
status.authentication_token = "authentication_token_str";
status.local_timestamp = "local_timestamp_str";

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

answer = stub.Ping(status)

print(answer)