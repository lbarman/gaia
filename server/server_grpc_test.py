from server_grpc import *
from time import sleep
import unittest
import grpc
import protobufs_pb2
import protobufs_pb2_grpc
from constants import *
import os.path
from database_test import dummy_config

def dummy_status_message():
    status = protobufs_pb2.Status()
    status.authentication_token = "authentication_token_str"
    status.local_timestamp = "local_timestamp_str"

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


class DummyServiceServicer(protobufs_pb2_grpc.GaiaServiceServicer):

    def Ping(self, request, context):
        answer = protobufs_pb2.Response()
        answer.action = protobufs_pb2.Response.DO_NOTHING
        config = answer.config
        config.feeding_module_activated = True
        config.watering_module_activated = True
        config.feeding_module_cronstring = "12h *"
        config.watering_module_cronstring = "13h 1,3,5"
        config.watering_pump_1_duration = 10
        config.watering_pump_2_duration = 20
        config.watering_pump_3_duration = 30
        config.watering_pump_4_duration = 40
        return answer


class GRPCServerTest(unittest.TestCase):

    def test_dummy(self):

        server = start_grpc_server(boot_type=GRPCServerBootingType.Dummy, verbose=True)
        sleep(1)

        # create the gRPC stub
        channel = grpc.insecure_channel('127.0.0.1:'+str(GRPC_SERVER_PORT))
        stub = protobufs_pb2_grpc.GaiaServiceStub(channel)

        # send message
        status = dummy_status_message()
        response = stub.Ping(status)

        self.assertEqual(response.action, protobufs_pb2.Response.DO_NOTHING)
        self.assertEqual(response.config.feeding_module_activated, True)
        self.assertEqual(response.config.watering_module_activated, True)
        self.assertEqual(response.config.feeding_module_cronstring, "12h *")
        self.assertEqual(response.config.watering_module_cronstring, "13h 1,3,5")
        self.assertEqual(response.config.watering_pump_1_duration, 10)
        self.assertEqual(response.config.watering_pump_2_duration, 20)
        self.assertEqual(response.config.watering_pump_3_duration, 30)
        self.assertEqual(response.config.watering_pump_4_duration, 40)

        server.stop(0)

    def test_real_inmemory(self):

        server = start_grpc_server(boot_type=GRPCServerBootingType.RealButInMemoryOnly, verbose=True)
        sleep(1)

        # create the gRPC stub
        channel = grpc.insecure_channel('127.0.0.1:'+str(GRPC_SERVER_PORT))
        stub = protobufs_pb2_grpc.GaiaServiceStub(channel)

        # send message
        status = dummy_status_message()
        response = stub.Ping(status)

        # this should be the default
        self.assertEqual(response.action, protobufs_pb2.Response.DO_NOTHING)
        self.assertEqual(response.HasField('config'), False)

        server.stop(0)

    def test_real_file(self):

        if os.path.isfile(SQLITE_DATABASE_PATH):
            self.skipTest("The file" + SQLITE_DATABASE_PATH + "already exists, cannot work with dirty data." +
                          "This test is meant for travis only. To force-run, delete the file manually.")

        db = Database(in_memory=False)
        db.recreate_database()

        # add a dummy command to the server
        config = dummy_config()
        db.save_command("REBOOT", config)

        server = start_grpc_server(boot_type=GRPCServerBootingType.Real, verbose=True)
        sleep(1)

        # create the gRPC stub
        channel = grpc.insecure_channel('127.0.0.1:'+str(GRPC_SERVER_PORT))
        stub = protobufs_pb2_grpc.GaiaServiceStub(channel)

        # send message
        status = dummy_status_message()
        response = stub.Ping(status)

        # this should be the default
        self.assertEqual(response.action, protobufs_pb2.Response.REBOOT)
        self.assertEqual(response.HasField('config'), True)

        self.assertEqual(response.config.feeding_module_activated, config.feeding_module_activated)
        self.assertEqual(response.config.watering_module_activated, config.feeding_module_activated)
        self.assertEqual(response.config.feeding_module_cronstring, config.feeding_module_cronstring)
        self.assertEqual(response.config.watering_module_cronstring, config.watering_module_cronstring)
        self.assertEqual(response.config.watering_pump_1_duration, config.watering_pump_1_duration)
        self.assertEqual(response.config.watering_pump_2_duration, config.watering_pump_2_duration)
        self.assertEqual(response.config.watering_pump_3_duration, config.watering_pump_3_duration)
        self.assertEqual(response.config.watering_pump_4_duration, config.watering_pump_4_duration)

        server.stop(0)


if __name__ == '__main__':
    unittest.main()
