from concurrent import futures
import time
import math

import grpc

from flask import Flask

from constants import *


webserver = Flask("GaiaWebServer")

@webserver.route('/')
def hello():
    return "Hello World!"

def startGRPCServer():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=GRPC_MAX_WORKERS))
    protobufs_pb2_grpc.add_GaiaServiceServicer_to_server(GaiaServiceServicer(), server)
    server.add_insecure_port('[::]:' + str(GRPC_SERVER_PORT))
    server.start()
    return server

def startWebServer():
    global webserver
    webserver.run(host='127.0.0.1', port=WEB_SERVER_PORT)

if __name__ == '__main__':
    gprcServer = startGRPCServer()
    try:
        while True:
            startWebServer() # blocking
    except KeyboardInterrupt:
        print("Quitting")
        gprcServer.stop(0)