from server_grpc import *
from time import sleep
import unittest
import grpc
import protobufs_pb2
import protobufs_pb2_grpc
from constants import *

def dummyProtobufStatusMessage():
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
    return status

class DummyServiceServicer(protobufs_pb2_grpc.GaiaServiceServicer):
    def Ping(self, request, context):
        answer = protobufs_pb2.Response()
        answer.action = protobufs_pb2.Response.DO_NOTHING
        config = answer.config;
        config.feeding_module_activated = True;
        config.watering_module_activated = True;
        config.feeding_module_cronstring = "12 *";
        config.watering_module_cronstring = "13 1,3,5";
        config.watering_pump_1_duration = 10;
        config.watering_pump_2_duration = 20;
        config.watering_pump_3_duration = 30;
        config.watering_pump_4_duration = 40;
        return answer

class GRPCServerTest(unittest.TestCase):

    def testBasicFunctionality(self):

        server = startGRPCServer(dummyServer=True)
        sleep(1)

        # create the gRPC stub
        channel = grpc.insecure_channel('127.0.0.1:'+str(GRPC_SERVER_PORT))
        stub = protobufs_pb2_grpc.GaiaServiceStub(channel)

        # send message
        status = dummyProtobufStatusMessage()
        answer = stub.Ping(status)

        self.assertEqual(answer.action, protobufs_pb2.Response.DO_NOTHING)
        self.assertEqual(answer.config.feeding_module_activated, True)
        self.assertEqual(answer.config.watering_module_activated, True)
        self.assertEqual(answer.config.feeding_module_cronstring, "12 *")
        self.assertEqual(answer.config.watering_module_cronstring, "13 1,3,5")
        self.assertEqual(answer.config.watering_pump_1_duration, 10)
        self.assertEqual(answer.config.watering_pump_2_duration, 20)
        self.assertEqual(answer.config.watering_pump_3_duration, 30)
        self.assertEqual(answer.config.watering_pump_4_duration, 40)

        server.stop(0)

if __name__ == '__main__':
    unittest.main()