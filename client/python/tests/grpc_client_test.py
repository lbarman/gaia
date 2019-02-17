import sys
import unittest
import os.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
import gaia_client.grpc_client as grpc_client
import gaia_client.database as database
import gaia_client.system as system
import gaia_client.protobufs_pb2 as protobufs_pb2
import gaia_client.protobufs_pb2_grpc as protobufs_pb2_grpc
import grpc
from concurrent import futures
from time import sleep

class SystemTest(unittest.TestCase):

    def test_client_creation(self):

        db = database.Database(in_memory=True)
        db.recreate_database()
        action_handler = DummyActionHandler()

        with self.assertRaises(ValueError):
            grpc_client.GRPC_Client(remote="localhost:12345", use_ssl=False, db=None, action_handler=action_handler)

        with self.assertRaises(ValueError):
            grpc_client.GRPC_Client(remote="localhost:12345", use_ssl=False, db=db, action_handler=None)

        with self.assertRaises(ValueError):
            grpc_client.GRPC_Client(remote="localhost:12345", use_ssl=False, db=None, action_handler=None)

        c = grpc_client.GRPC_Client(remote="localhost:12345", use_ssl=False, db=db, action_handler=action_handler)
        self.assertNotEqual(c, None)

        # assert that this does not crash
        c.handle_response(None)

        # assert that this does not cause any action
        answer = protobufs_pb2.Response()
        answer.action = protobufs_pb2.Response.DO_NOTHING
        c.handle_response(answer)

        self.assertEqual(action_handler.n_shutdown, 0)
        self.assertEqual(action_handler.n_reboot, 0)
        self.assertEqual(action_handler.n_feed, 0)
        self.assertEqual(action_handler.n_water, 0)
        self.assertEqual(action_handler.n_reset_db, 0)


    def test_config_store(self):

        db = database.Database(in_memory=True)
        db.recreate_database()
        action_handler = DummyActionHandler()

        c = grpc_client.GRPC_Client(remote="localhost:12345", use_ssl=False, db=db, action_handler=action_handler)

        self.assertEqual(db.get_config(), None)

        # assert that this does not cause any action
        answer = protobufs_pb2.Response()
        answer.action = protobufs_pb2.Response.DO_NOTHING

        #no config in this message
        c.handle_response(answer)

        self.assertEqual(action_handler.n_shutdown, 0)
        self.assertEqual(action_handler.n_reboot, 0)
        self.assertEqual(action_handler.n_feed, 0)
        self.assertEqual(action_handler.n_water, 0)
        self.assertEqual(action_handler.n_reset_db, 0)
        self.assertEqual(db.get_config(), None)

    def test_config_store(self):

        db = database.Database(in_memory=True)
        db.recreate_database()
        action_handler = DummyActionHandler()

        c = grpc_client.GRPC_Client(remote="localhost:12345", use_ssl=False, db=db, action_handler=action_handler)

        self.assertEqual(db.get_config(), None)

        # assert that this does not cause any action
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

        c.handle_response(answer)

        self.assertEqual(action_handler.n_shutdown, 0)
        self.assertEqual(action_handler.n_reboot, 0)
        self.assertEqual(action_handler.n_feed, 0)
        self.assertEqual(action_handler.n_water, 0)
        self.assertEqual(action_handler.n_reset_db, 0)
        self.assertNotEqual(db.get_config(), None)

        config2 = db.get_config()
        self.assertEqual(config2['feeding_module_activated'], config.feeding_module_activated)
        self.assertEqual(config2['watering_module_activated'], config.watering_module_activated)
        self.assertEqual(config2['feeding_module_cronstring'], config.feeding_module_cronstring)
        self.assertEqual(config2['watering_module_cronstring'], config.watering_module_cronstring)
        self.assertEqual(config2['watering_pump_1_duration'], config.watering_pump_1_duration)
        self.assertEqual(config2['watering_pump_2_duration'], config.watering_pump_2_duration)
        self.assertEqual(config2['watering_pump_3_duration'], config.watering_pump_3_duration)
        self.assertEqual(config2['watering_pump_4_duration'], config.watering_pump_4_duration)


    def test_shutdown(self):

        db = database.Database(in_memory=True)
        db.recreate_database()
        action_handler = DummyActionHandler()

        c = grpc_client.GRPC_Client(remote="localhost:12345", use_ssl=False, db=db, action_handler=action_handler)

        self.assertEqual(db.get_config(), None)

        # assert that this does not cause any action
        answer = protobufs_pb2.Response()
        answer.action = protobufs_pb2.Response.SHUTDOWN

        #no config in this message
        c.handle_response(answer)

        self.assertEqual(action_handler.n_shutdown, 1)
        self.assertEqual(action_handler.n_reboot, 0)
        self.assertEqual(action_handler.n_feed, 0)
        self.assertEqual(action_handler.n_water, 0)
        self.assertEqual(action_handler.n_reset_db, 0)
        self.assertEqual(db.get_config(), None)

    def test_reboot(self):

        db = database.Database(in_memory=True)
        db.recreate_database()
        action_handler = DummyActionHandler()

        c = grpc_client.GRPC_Client(remote="localhost:12345", use_ssl=False, db=db, action_handler=action_handler)

        self.assertEqual(db.get_config(), None)

        # assert that this does not cause any action
        answer = protobufs_pb2.Response()
        answer.action = protobufs_pb2.Response.REBOOT

        #no config in this message
        c.handle_response(answer)

        self.assertEqual(action_handler.n_shutdown, 0)
        self.assertEqual(action_handler.n_reboot, 1)
        self.assertEqual(action_handler.n_feed, 0)
        self.assertEqual(action_handler.n_water, 0)
        self.assertEqual(action_handler.n_reset_db, 0)
        self.assertEqual(db.get_config(), None)


    def test_against_server(self):

        port = 50051

        servicer = DummyServiceServicer1()
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
        protobufs_pb2_grpc.add_GaiaServiceServicer_to_server(servicer, server)
        server.add_insecure_port('[::]:' + str(port))
        server.start()

        sleep(1)

        db = database.Database(in_memory=True)
        db.recreate_database()
        action_handler = DummyActionHandler()
        c = grpc_client.GRPC_Client(remote='127.0.0.1:'+str(port), use_ssl=False, db=db, action_handler=action_handler)

        self.assertNotEqual(c, None)

        temp = dict()
        temp['t1'] = 0
        temp['humidity'] = 1
        temp['t2'] = 2
        temp['t3'] = 3

        # try writing a message
        m = c.build_status_message(temperature_sensors=temp, system_status=system.get_system_status())
        answer = c.send_status_message(status_message=m)

        # assert that we got a response
        self.assertEqual(answer.action, protobufs_pb2.Response.DO_NOTHING)
        self.assertTrue(answer.HasField('config'))

        # assert that response is treated correctly
        c.handle_response(answer)

        self.assertEqual(action_handler.n_shutdown, 0)
        self.assertEqual(action_handler.n_reboot, 0)
        self.assertEqual(action_handler.n_feed, 0)
        self.assertEqual(action_handler.n_water, 0)
        self.assertEqual(action_handler.n_reset_db, 0)
        self.assertNotEqual(db.get_config(), None)

        config2 = db.get_config()
        config = answer.config
        self.assertEqual(config2['feeding_module_activated'], config.feeding_module_activated)
        self.assertEqual(config2['watering_module_activated'], config.watering_module_activated)
        self.assertEqual(config2['feeding_module_cronstring'], config.feeding_module_cronstring)
        self.assertEqual(config2['watering_module_cronstring'], config.watering_module_cronstring)
        self.assertEqual(config2['watering_pump_1_duration'], config.watering_pump_1_duration)
        self.assertEqual(config2['watering_pump_2_duration'], config.watering_pump_2_duration)
        self.assertEqual(config2['watering_pump_3_duration'], config.watering_pump_3_duration)
        self.assertEqual(config2['watering_pump_4_duration'], config.watering_pump_4_duration)

        server.stop(0)


    def test_against_server2(self):

        port = 50051

        servicer = DummyServiceServicer2()
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
        protobufs_pb2_grpc.add_GaiaServiceServicer_to_server(servicer, server)
        server.add_insecure_port('[::]:' + str(port))
        server.start()

        sleep(1)

        db = database.Database(in_memory=True)
        db.recreate_database()
        action_handler = DummyActionHandler()
        c = grpc_client.GRPC_Client(remote='127.0.0.1:'+str(port), use_ssl=False, db=db, action_handler=action_handler)

        self.assertNotEqual(c, None)

        # try writing a message
        m = c.build_status_message(temperature_sensors=None)
        answer = c.send_status_message(status_message=m)

        # assert that we got a response
        self.assertEqual(answer.action, protobufs_pb2.Response.REBOOT)
        self.assertFalse(answer.HasField('config'))

        # assert that response is treated correctly
        c.handle_response(answer)

        self.assertEqual(action_handler.n_shutdown, 0)
        self.assertEqual(action_handler.n_reboot, 1)
        self.assertEqual(action_handler.n_feed, 0)
        self.assertEqual(action_handler.n_water, 0)
        self.assertEqual(action_handler.n_reset_db, 0)
        self.assertEqual(db.get_config(), None)

        server.stop(0)

    def test_action_creation(self):

        port = 50051

        db = database.Database(in_memory=True)
        db.recreate_database()
        action_handler = grpc_client.ActionHandler()
        c = grpc_client.GRPC_Client(remote='127.0.0.1:'+str(port), use_ssl=False, db=db, action_handler=action_handler)


        with self.assertRaises(ValueError):
            c.build_action_report_message(action="somestring", action_details="a long string")

        res = c.build_action_report_message(action="FEEDING", action_details=None)
        self.assertNotEqual(res, None)
        self.assertEqual(res.action, protobufs_pb2.ActionReport.FEEDING)
        self.assertEqual(res.action_details, "")

        res = c.build_action_report_message(action="WATERING", action_details="some string")
        self.assertNotEqual(res, None)
        self.assertEqual(res.action, protobufs_pb2.ActionReport.WATERING)
        self.assertEqual(res.action_details, "some string")

    def test_action_report(self):

        port = 50051

        servicer = DummyServiceServicer2()
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
        protobufs_pb2_grpc.add_GaiaServiceServicer_to_server(servicer, server)
        server.add_insecure_port('[::]:' + str(port))
        server.start()

        sleep(1)

        db = database.Database(in_memory=True)
        db.recreate_database()
        action_handler = DummyActionHandler()
        c = grpc_client.GRPC_Client(remote='127.0.0.1:'+str(port), use_ssl=False, db=db, action_handler=action_handler)

        self.assertNotEqual(c, None)

        # try writing a message
        m = c.build_action_report_message(action="FEEDING", action_details="a long string")
        answer = c.send_action_report_message(action_report=m)

        # assert that we got a response
        self.assertEqual(answer.action, protobufs_pb2.Response.DO_NOTHING)
        self.assertFalse(answer.HasField('config'))

        # assert that response is treated correctly
        c.handle_response(answer)

        self.assertEqual(action_handler.n_shutdown, 0)
        self.assertEqual(action_handler.n_reboot, 0)
        self.assertEqual(action_handler.n_feed, 0)
        self.assertEqual(action_handler.n_water, 0)
        self.assertEqual(action_handler.n_reset_db, 0)
        self.assertEqual(db.get_config(), None)

        server.stop(0)

    def test_no_error(self):

        # should not crash if server is unreachable
        port = 50051

        db = database.Database(in_memory=True)
        db.recreate_database()
        action_handler = DummyActionHandler()
        c = grpc_client.GRPC_Client(remote='127.0.0.1:'+str(port), use_ssl=False, db=db, action_handler=action_handler)

        self.assertNotEqual(c, None)

        # try writing a message
        m = c.build_status_message(temperature_sensors=None)
        answer = c.send_status_message(status_message=m)
        self.assertEqual(answer, None)

        # try writing a message
        m = c.build_action_report_message(action="FEEDING", action_details="a long string")
        answer = c.send_action_report_message(action_report=m)
        self.assertEqual(answer, None)


class DummyActionHandler(grpc_client.ActionHandler):

    n_shutdown = 0
    n_reboot = 0
    n_feed = 0
    n_water = 0
    n_reset_db = 0

    def handle(self, action):
        if action == protobufs_pb2.Response.DO_NOTHING:
            return
        if action == protobufs_pb2.Response.SHUTDOWN:
            self.n_shutdown += 1
        elif action == protobufs_pb2.Response.REBOOT:
            self.n_reboot += 1
        elif action == protobufs_pb2.Response.FEED:
            self.n_feed += 1
        elif action == protobufs_pb2.Response.WATER:
            self.n_water += 1
        elif action == protobufs_pb2.Response.DELETE_DB:
            self.n_reset_db += 1
        else:
            print("Warning: unknown action", action, "doing nothing")

class DummyServiceServicer1(protobufs_pb2_grpc.GaiaServiceServicer):

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


class DummyServiceServicer2(protobufs_pb2_grpc.GaiaServiceServicer):

    def Ping(self, request, context):
        answer = protobufs_pb2.Response()
        answer.action = protobufs_pb2.Response.REBOOT
        return answer

    def ActionDone(self, request, context):
        answer = protobufs_pb2.Response()
        answer.action = protobufs_pb2.Response.DO_NOTHING
        return answer

if __name__ == '__main__':
    unittest.main()
