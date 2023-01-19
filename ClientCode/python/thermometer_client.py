#from __future__ import print_function

import logging

import grpc
import iot_service_pb2
import iot_service_pb2_grpc

from const import *


def run():
    with grpc.insecure_channel(GRPC_SERVER+':'+GRPC_PORT) as channel:
        stub = iot_service_pb2_grpc.IoTServiceStub(channel)
        response = stub.GetAccessToken(iot_service_pb2.Credentials(login='Alice', password='123456'))
        print(response.status)
        if response.status == "acesso concedido":
            token = response.token
            response = stub.SayTemperature(iot_service_pb2.TemperatureRequest(sensorName='temperature-1', accessToken=token))
            print(response.status)
            print("Temperature received: " + response.temperature)

if __name__ == '__main__':
    logging.basicConfig()
    run()
