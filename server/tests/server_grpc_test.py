import sys
import os.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
import gaia_server.server_grpc as server_grpc
from time import sleep
import unittest
import grpc
import os.path
from datetime import datetime
import gaia_server.protobufs_pb2 as protobufs_pb2
import gaia_server.protobufs_pb2_grpc as protobufs_pb2_grpc
import gaia_server.database as database
import gaia_server.constants as constants
import tests.database_test as database_test
import pytest

def dummy_action_report():
    action_report = protobufs_pb2.ActionReport()
    action_report.local_timestamp = datetime(2009, 12, 1, 19, 31, 1, 40113).strftime("%Y-%m-%d %H:%M:%S")
    action_report.action = protobufs_pb2.ActionReport.FEEDING
    action_report.action_details = "a long string"
    action_report.authentication_token = 'invalid'
    return action_report

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

    def ActionDone(self, request, context):
        answer = protobufs_pb2.Response()
        answer.action = protobufs_pb2.Response.DO_NOTHING
        return answer


class GRPCServerTest(unittest.TestCase):

    def test_dummy(self):

        servicer = DummyServiceServicer()
        server = server_grpc.start_grpc_server(override_servicer=servicer, verbose=True)
        sleep(1)

        # create the gRPC stub
        channel = grpc.insecure_channel('127.0.0.1:'+str(constants.GRPC_SERVER_PORT))
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

    def test_real_in_memory_wrong_auth(self):

        servicer = server_grpc.GaiaServiceServicer(real_database=False, verbose=True)
        server = server_grpc.start_grpc_server(override_servicer=servicer, verbose=True)
        sleep(1)

        # create the gRPC stub
        channel = grpc.insecure_channel('127.0.0.1:'+str(constants.GRPC_SERVER_PORT))
        stub = protobufs_pb2_grpc.GaiaServiceStub(channel)

        # send message

        with pytest.raises(Exception):
            response = stub.Ping(dummy_status_message())
            assert response is None

        with pytest.raises(Exception):
            response = stub.ActionDone(dummy_action_report())
            assert response is None

        server.stop(0)

    def test_real_in_memory_valid_auth(self):

        servicer = server_grpc.GaiaServiceServicer(real_database=False, verbose=True)
        server = server_grpc.start_grpc_server(override_servicer=servicer, verbose=True)
        sleep(1)

        # create the gRPC stub
        channel = grpc.insecure_channel('127.0.0.1:'+str(constants.GRPC_SERVER_PORT))
        stub = protobufs_pb2_grpc.GaiaServiceStub(channel)

        # send message
        status = dummy_status_message()
        status.authentication_token = constants.AUTHENTICATION_TOKEN
        response = stub.Ping(status)

        # this should be the default
        self.assertEqual(response.action, protobufs_pb2.Response.DO_NOTHING)
        self.assertEqual(response.HasField('config'), False)

        # send message
        report = dummy_action_report()
        report.authentication_token = constants.AUTHENTICATION_TOKEN
        response = stub.ActionDone(report)

        # this should be the default
        self.assertEqual(response.action, protobufs_pb2.Response.DO_NOTHING)
        self.assertEqual(response.HasField('config'), False)

        server.stop(0)

    def test_real_file_wrong_auth_auth(self):

        db = database.Database(in_memory=False)
        db.recreate_database()

        # add a dummy command to the server
        config = database_test.dummy_config()
        db.save_command("REBOOT", config)

        server = server_grpc.start_grpc_server(verbose=True)
        sleep(1)

        # create the gRPC stub
        channel = grpc.insecure_channel('127.0.0.1:'+str(constants.GRPC_SERVER_PORT))
        stub = protobufs_pb2_grpc.GaiaServiceStub(channel)

        with pytest.raises(Exception):
            response = stub.Ping(dummy_status_message())
            assert response is None

        with pytest.raises(Exception):
            response = stub.ActionDone(dummy_action_report())
            assert response is None

        server.stop(0)

    def test_real_file_valid_auth(self):

        db = database.Database(in_memory=False)
        db.recreate_database()

        # add a dummy command to the server
        config = database_test.dummy_config()
        db.save_command("REBOOT", config)

        server = server_grpc.start_grpc_server(verbose=True)
        sleep(1)

        # create the gRPC stub
        channel = grpc.insecure_channel('127.0.0.1:'+str(constants.GRPC_SERVER_PORT))
        stub = protobufs_pb2_grpc.GaiaServiceStub(channel)

        # send message
        status = dummy_status_message()
        status.authentication_token = constants.AUTHENTICATION_TOKEN
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

        # send message
        report = dummy_action_report()
        report.authentication_token = constants.AUTHENTICATION_TOKEN
        response = stub.ActionDone(report)

        # this should be the default
        self.assertEqual(response.action, protobufs_pb2.Response.DO_NOTHING)
        self.assertEqual(response.HasField('config'), False)

        server.stop(0)


if __name__ == '__main__':
    unittest.main()
