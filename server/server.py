# Copyright 2015 gRPC authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""The Python implementation of the gRPC route guide server."""

from concurrent import futures
import time
import math

import grpc

import protobufs_pb2
import protobufs_pb2_grpc
from flask import Flask

class GaiaServiceServicer(protobufs_pb2_grpc.GaiaServiceServicer):
    """Provides methods that implement functionality of route guide server."""

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


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
    protobufs_pb2_grpc.add_GaiaServiceServicer_to_server(GaiaServiceServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    try:
        while True:
            print("OK, sleeping...")
            time.sleep(60 * 60 * 24)
    except KeyboardInterrupt:
        server.stop(0)


app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello World!"

if __name__ == '__main__':
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
    protobufs_pb2_grpc.add_GaiaServiceServicer_to_server(GaiaServiceServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    try:
        while True:
            print("OK, now starting flask...")
            app.run()
    except KeyboardInterrupt:
        server.stop(0)