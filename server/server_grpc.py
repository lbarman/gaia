from concurrent import futures
import grpc
import protobufs_pb2
import protobufs_pb2_grpc
from server_grpc_test import DummyServiceServicer
from database import Database
from time import sleep
from constants import GRPC_MAX_WORKERS, GRPC_SERVER_PORT
from enum import Enum

_ONE_DAY_IN_SECONDS = 60 * 60 * 24


class GaiaServiceServicer(protobufs_pb2_grpc.GaiaServiceServicer):

    def __init__(self, real_database=True, verbose=False):
        self.useRealDatabase = real_database
        self.verbose = verbose

    def Ping(self, status, context):

        db = None
        if self.useRealDatabase:
            db = Database(in_memory=False)  # sql schema was already instanciated
        else:
            db = Database(in_memory=True)
            db.recreate_database()

        if self.verbose:
            print("Got query", status, context)

        db.save_status(status)

        # prepare empty response
        response = protobufs_pb2.Response()
        response.action = protobufs_pb2.Response.DO_NOTHING

        # check if we have to transmit a command
        command = db.get_command()
        if command is not None:
            if command['action'] == 'SHUTDOWN':
                    response.action = protobufs_pb2.Response.SHUTDOWN
            elif command['action'] == 'REBOOT':
                    response.action = protobufs_pb2.Response.REBOOT

            if command['config'] is not None:
                response.config.feeding_module_activated = command['config']['feeding_module_activated']
                response.config.watering_module_activated = command['config']['watering_module_activated']
                response.config.feeding_module_cronstring = command['config']['feeding_module_cronstring']
                response.config.watering_module_cronstring = command['config']['watering_module_cronstring']
                response.config.watering_pump_1_duration = command['config']['watering_pump_1_duration']
                response.config.watering_pump_2_duration = command['config']['watering_pump_2_duration']
                response.config.watering_pump_3_duration = command['config']['watering_pump_3_duration']
                response.config.watering_pump_4_duration = command['config']['watering_pump_4_duration']

        db.delete_all_commands()

        if self.verbose:
            print("Answering with", response)

        return response


class GRPCServerBootingType(Enum):
    Real = 0
    RealButInMemoryOnly = 1
    Dummy = 2


def start_grpc_server(boot_type=GRPCServerBootingType.Real, verbose=False):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=GRPC_MAX_WORKERS))

    servicer = None

    if boot_type == GRPCServerBootingType.Real:
        servicer = GaiaServiceServicer(real_database=True, verbose=verbose)
    elif boot_type == GRPCServerBootingType.RealButInMemoryOnly:
        servicer = GaiaServiceServicer(real_database=False, verbose=verbose)
    elif boot_type == GRPCServerBootingType.Dummy:
        servicer = DummyServiceServicer()

    protobufs_pb2_grpc.add_GaiaServiceServicer_to_server(servicer, server)
    server.add_insecure_port('[::]:' + str(GRPC_SERVER_PORT))
    server.start()
    return server


if __name__ == '__main__':
    # try recreating the DB
    db = Database()
    db.recreate_database()

    gprcServer = start_grpc_server()
    try:
        while True:
            sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        print("Quitting")
        gprcServer.stop(0)
