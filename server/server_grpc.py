from concurrent import futures
import time
import math

import grpc
import sqlite3

import protobufs_pb2
import protobufs_pb2_grpc
from server_grpc_test import DummyServiceServicer
from constants import *
from database import *

_ONE_DAY_IN_SECONDS = 60 * 60 * 24

class GaiaServiceServicer(protobufs_pb2_grpc.GaiaServiceServicer):
    def Ping(self, request, context):
        print("Got query", request, context)
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
        print("Answering with", answer, protobufs_pb2.Response.REBOOT)
        return answer

def startGRPCServer(dummyServer=False):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=GRPC_MAX_WORKERS))

    servicer = GaiaServiceServicer()
    if dummyServer:
        servicer = DummyServiceServicer()

    protobufs_pb2_grpc.add_GaiaServiceServicer_to_server(servicer, server)
    server.add_insecure_port('[::]:' + str(GRPC_SERVER_PORT))
    server.start()
    return server

if __name__ == '__main__':
    gprcServer = startGRPCServer()
    try:
        while True:
            sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        print("Quitting")
        gprcServer.stop(0)