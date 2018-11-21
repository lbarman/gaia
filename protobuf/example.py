# allow imports from one level up
import sys
import os.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

import protobufs_pb2

if len(sys.argv) != 2:
    print("Usage: write.py out_file")
    sys.exit(1)

out_file = sys.argv[1]

# creates and writes a Protobuf file
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

binaryOut = status.SerializeToString()
with open(out_file, "bw") as f:
    f.write(binaryOut)

# print bytes
print(binaryOut)

# try re-reading it
f = open(out_file, "rb")
binaryString = f.read()
f.close()

status2 = protobufs_pb2.Status()
status2.ParseFromString(binaryString)
print(status2)