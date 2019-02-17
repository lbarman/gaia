import gaia_client.constants as constants
import gaia_client.database as database
import grpc
import gaia_client.protobufs_pb2 as protobufs_pb2
import gaia_client.protobufs_pb2_grpc as protobufs_pb2_grpc
from datetime import datetime


class GRPC_Client:

    remote_server_address = ""
    use_ssl = False
    db = None
    action_handler = None

    # instantiated channel
    grpc_channel = None
    grpc_stub = None

    def __init__(self, remote=constants.GAIA_GRPC_URL, use_ssl=constants.GAIA_GRPC_USE_SSL, db=None, action_handler=None):

        self.remote_server_address = remote
        self.use_ssl = use_ssl

        if db is None or not isinstance(db, database.Database):
            raise ValueError("db cannot be null, and must be a Database")
        if action_handler is None or not isinstance(action_handler, ActionHandler):
            raise ValueError("action_handler cannot be null, and must be a ActionHandler")

        self.db = db
        self.action_handler = action_handler

        if use_ssl:
            # do be correct, we should pin the .crt file from the server here
            credentials = grpc.ssl_channel_credentials(root_certificates=None)
            self.grpc_channel = grpc.secure_channel(remote, credentials)
        else:
            self.grpc_channel = grpc.insecure_channel(remote)

        self.grpc_stub = protobufs_pb2_grpc.GaiaServiceStub(self.grpc_channel)

    def build_status_message(self, temperature_sensors=None, system_status=None):
        status = protobufs_pb2.Status()
        status.authentication_token = constants.GAIA_SECRETTOKEN
        status.local_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # feed temperature info
        if temperature_sensors is not None:
            status.temperature = temperature_sensors['t1']
            status.humidity = temperature_sensors['humidity']
            status.temperature2 = temperature_sensors['t2']
            status.temperature3 = temperature_sensors['t3']
        else:
            status.temperature = 0
            status.humidity = 0
            status.temperature2 = 0
            status.temperature3 = 0

        # feed config
        config = self.db.get_config()
        config2 = status.current_config

        if config is not None:
            config2.feeding_module_activated = config['feeding_module_activated']
            config2.watering_module_activated = config['watering_module_activated']
            config2.feeding_module_cronstring = config['feeding_module_cronstring']
            config2.watering_module_cronstring = config['watering_module_cronstring']
            config2.watering_pump_1_duration = config['watering_pump_1_duration']
            config2.watering_pump_2_duration = config['watering_pump_2_duration']
            config2.watering_pump_3_duration = config['watering_pump_3_duration']
            config2.watering_pump_4_duration = config['watering_pump_4_duration']
        else:
            config2.feeding_module_activated = constants.FEEDING_DEFAULT_ENABLED
            config2.watering_module_activated = constants.WATERING_DEFAULT_ENABLED
            config2.feeding_module_cronstring = constants.FEEDING_DEFAULT_CRONSTRING
            config2.watering_module_cronstring = constants.WATERING_DEFAULT_CRONSTRING
            config2.watering_pump_1_duration = int(constants.WATER_PLANT_RELAY1_DURATION)
            config2.watering_pump_2_duration = int(constants.WATER_PLANT_RELAY2_DURATION)
            config2.watering_pump_3_duration = int(constants.WATER_PLANT_RELAY3_DURATION)
            config2.watering_pump_4_duration = int(constants.WATER_PLANT_RELAY4_DURATION)

        # feed system infos
        system_status2 = status.system_status
        if system_status is not None:
            system_status2.uptime = system_status['uptime']
            system_status2.memory = system_status['memory']
            system_status2.disk_usage = system_status['disk_usage']
            system_status2.processes = system_status['processes']
        else:
            system_status2.uptime = "?"
            system_status2.memory = "?"
            system_status2.disk_usage = "?"
            system_status2.processes = "?"

        return status

    def build_action_report_message(self, action="", action_details=""):
        action_report = protobufs_pb2.ActionReport()
        action_report.authentication_token = constants.GAIA_SECRETTOKEN
        action_report.local_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if action == "FEEDING":
            action_report.action = protobufs_pb2.ActionReport.FEEDING
        elif action == "WATERING":
            action_report.action = protobufs_pb2.ActionReport.WATERING
        else:
            raise ValueError("action must be FEEDING or WATERING")

        if action_details is None:
            action_details = ""

        action_report.action_details = action_details

        return action_report

    # returns a protobuf Response, or None
    def send_status_message(self, status_message=None):
        try:
            response = self.grpc_stub.Ping(status_message)
            return response
        except Exception as e:
            print("Can't send Status to Gaia GRPC server on " + self.remote_server_address + " using ssl " + str(self.use_ssl) + ", reason: " + str(e))
        return None

    # returns a protobuf Response, or None
    def send_action_report_message(self, action_report=None):
        try:
            response = self.grpc_stub.ActionDone(action_report)
            return response
        except Exception as e:
            print("Can't send ActionDone to Gaia GRPC server on " + self.remote_server_address + " using ssl " + str(
                self.use_ssl) + ", reason: " + str(e))
        return None

    def handle_response(self, response=None):
        if response is None:
            return

        # check if config update
        if response.HasField('config'):
            print("Saving new config ", response.config)
            self.db.save_config(response.config)

        self.action_handler.handle(response.action)


class ActionHandler:

    noop = lambda: None

    action_shutdown = noop
    action_reboot = noop
    action_feed = noop
    action_water = noop
    action_reset_db = noop

    def __init__(self, shutdown_fn=noop, reboot_fn=noop, feed_fn=noop, water_fn=noop, reset_db_fn=noop):
        self.action_shutdown = shutdown_fn
        self.action_reboot = reboot_fn
        self.action_feed = feed_fn
        self.action_water = water_fn
        self.action_reset_db = reset_db_fn

    def handle(self, action):
        if action == protobufs_pb2.Response.DO_NOTHING:
            return
        if action == protobufs_pb2.Response.SHUTDOWN:
            self.action_shutdown()
        elif action == protobufs_pb2.Response.REBOOT:
            self.action_reboot()
        elif action == protobufs_pb2.Response.FEED:
            self.action_feed()
        elif action == protobufs_pb2.Response.WATER:
            self.action_water()
        elif action == protobufs_pb2.Response.DELETE_DB:
            self.action_reset_db()
        else:
            print("Warning: unknown action", action, "doing nothing")