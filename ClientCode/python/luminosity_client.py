#from __future__ import print_function

import logging

import grpc
import iot_service_pb2
import iot_service_pb2_grpc

from const import *


def run():
    with grpc.insecure_channel(GRPC_SERVER+':'+GRPC_PORT) as channel:
        stub = iot_service_pb2_grpc.IoTServiceStub(channel)
        response = stub.GetAccessToken(iot_service_pb2.Credentials(login='Bob', password='qwert'))
        print(response.status)
        if response.status == "acesso concedido":
            token = response.token
            response = stub.SayLuminosity(iot_service_pb2.TemperatureRequest(sensorName='luminosity-1', accessToken=token))
            print(response.status)
            print("Luminosity received: " + response.luminosity)

if __name__ == '__main__':
    logging.basicConfig()
    run()
