import threading
from concurrent import futures
import logging

from const import *
from kafka import KafkaConsumer, KafkaProducer
import grpc
import iot_service_pb2
import iot_service_pb2_grpc

# Twin state
current_temperature = 'void'
led_state = {'red': 0, 'green': 0}

# Kafka consumer to run on a separate thread


def consume_temperature():
    global current_temperature
    consumer = KafkaConsumer(bootstrap_servers=KAFKA_SERVER+':'+KAFKA_PORT)
    consumer.subscribe(topics=('temperature'))
    for msg in consumer:
        print(msg.value.decode())
        current_temperature = msg.value.decode()


def produce_led_command(state, ledname):
    producer = KafkaProducer(bootstrap_servers=KAFKA_SERVER+':'+KAFKA_PORT)
    producer.send('ledcommand', key=ledname.encode(),
                  value=str(state).encode())
    return state


class IoTServer(iot_service_pb2_grpc.IoTServiceServicer):
    usersDB = {"Alice": "123456", "Bob": "qwert"}
    accessToken = {
        "Alice": "69ace8a2-96a6-11ed-a1eb-0242ac120002",
        "Bob": "73a25f82-96aa-11ed-a1eb-0242ac120002",
    }
    authorizations = {
        "69ace8a2-96a6-11ed-a1eb-0242ac120002": ["led-1", "temperature-1"],
        "73a25f82-96aa-11ed-a1eb-0242ac120002": ["led-1", "led-2", "luminosity-1"]
    }

    def GetAccessToken(self, request, context):
        login = request.login
        password = request.password
        accessGranted = False
        if login in self.usersDB:
            if self.usersDB[login] == password:
                accessGranted = True

        if accessGranted:
            token = self.accessToken[login][0]
            return iot_service_pb2.Token(status="acesso concedido", token=token)
        else:
            return iot_service_pb2.Token(status="acesso negado", token="")

    def SayTemperature(self, request, context):
        if request.accessToken == self.accessToken:
            return iot_service_pb2.TemperatureReply(status="Ok", temperature=current_temperature)
        else:
            return iot_service_pb2.TemperatureReply(status="Erro de acesso", temperature="")

    def BlinkLed(self, request, context):
        print("Blink led ", request.ledname)
        print("...with state ", request.state)
        produce_led_command(request.state, request.ledname)
        # Update led state of twin
        led_state[request.ledname] = request.state
        return iot_service_pb2.LedReply(ledstate=led_state)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    iot_service_pb2_grpc.add_IoTServiceServicer_to_server(IoTServer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    trd = threading.Thread(target=consume_temperature)
    trd.start()
    # Initialize the state of the leds on the actual device
    for color in led_state.keys():
        produce_led_command(led_state[color], color)
    serve()
