#from __future__ import print_function

import logging
import sys

import grpc
import iot_service_pb2
import iot_service_pb2_grpc

from const import *


def run():
    with grpc.insecure_channel(GRPC_SERVER + ':' + GRPC_PORT) as channel:
        stub = iot_service_pb2_grpc.IoTServiceStub (channel)
        response = stub.GetAccessToken(iot_service_pb2.Credentials(login='Alice', password='123456'))
        print(response.status)
        if response.status == "acesso concedido":
            token = response.token
            response = stub.BlinkLed(iot_service_pb2.LedRequest(state=int(sys.argv[1]), sensorName=sys.argv[2], accessToken=token))
            print(response.status)
            if response.status == 'Erro de autorização':
                sys.exit(0)

            if response.ledstate[sys.argv[2]] == 1:
                print("Led state is on")
            else:
                print("Led state is off")

if __name__ == '__main__':
    logging.basicConfig()
    run()
