from concurrent import futures
from time import sleep

import grpc

import gaia_server.constants as constants
import gaia_server.database as database
import gaia_server.protobufs_pb2_grpc as protobufs_pb2
import gaia_server.protobufs_pb2_grpc as protobufs_pb2_grpc

_ONE_DAY_IN_SECONDS = 60 * 60 * 24


class GaiaServiceServicer(protobufs_pb2_grpc.GaiaServiceServicer):

    def __init__(self, real_database=True, verbose=False):
        self.useRealDatabase = real_database
        self.verbose = verbose

    def Ping(self, status, context):

        db = None
        if self.useRealDatabase:
            db = database.Database(in_memory=False)  # sql schema was already instanciated
        else:
            db = database.Database(in_memory=True)
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
            if command['text'] == 'SHUTDOWN':
                    response.action = protobufs_pb2.Response.SHUTDOWN
            elif command['text'] == 'REBOOT':
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

def start_grpc_server(override_servicer=None, verbose=False):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=constants.GRPC_MAX_WORKERS))

    servicer = None

    if override_servicer == None:
        servicer = GaiaServiceServicer(real_database=True, verbose=verbose)
    else:
        servicer = override_servicer

    protobufs_pb2_grpc.add_GaiaServiceServicer_to_server(servicer, server)
    server.add_insecure_port('[::]:' + str(constants.GRPC_SERVER_PORT))
    print("Starting gRPC server on port", constants.GRPC_SERVER_PORT)
    server.start()
    return server


if __name__ == '__main__':
    # try recreating the DB
    db = database.Database()
    db.recreate_database()

    gprcServer = start_grpc_server()
    try:
        while True:
            sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        print("Quitting")
        gprcServer.stop(0)
