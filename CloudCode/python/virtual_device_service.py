import threading
from concurrent import futures
import logging
import pickle

from const import *
from kafka import KafkaConsumer, KafkaProducer
import grpc
import iot_service_pb2
import iot_service_pb2_grpc

# Twin state
current_temperatures = {"temperature-1": "void", "temperature-2": "void"}
current_luminosities = {"luminosity-1": "void", "luminosity-2": "void"}
led_state = {'red': 0, 'green': 0}


# Kafka consumer to run on a separate thread
def consume_temperature():
    global current_temperatures
    consumer = KafkaConsumer(bootstrap_servers=KAFKA_SERVER + ':' + KAFKA_PORT)
    consumer.subscribe(topics=('temperature'))
    for msg in consumer:
        current_temperatures[msg.key.decode()] = msg.value.decode()
        print(current_temperatures)


# Kafka consumer to run on a separate thread
def consume_luminosity():
    global current_luminosities
    consumer = KafkaConsumer(bootstrap_servers=KAFKA_SERVER + ':' + KAFKA_PORT)
    consumer.subscribe(topics=('luminosity'))
    for msg in consumer:
        current_luminosities[msg.key.decode()] = msg.value.decode()
        print(current_luminosities)


def produce_led_command(state, ledname):
    producer = KafkaProducer(bootstrap_servers=KAFKA_SERVER + ':' + KAFKA_PORT)
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
        "69ace8a2-96a6-11ed-a1eb-0242ac120002": ["led-red", "temperature-1"],
        "73a25f82-96aa-11ed-a1eb-0242ac120002": ["led-red", "led-green", "luminosity-1"]
    }

    def GetAccessToken(self, request, context):
        login = request.login
        password = request.password
        print(login, password)
        accessGranted = False
        if login in self.usersDB:
            if self.usersDB[login] == password:
                accessGranted = True

        if accessGranted:
            token = self.accessToken[login]
            return iot_service_pb2.Token(status="acesso concedido", token=token)
        else:
            return iot_service_pb2.Token(status="acesso negado", token="")

    def SayTemperature(self, request, context):
        if request.accessToken in self.authorizations:
            if request.sensorName in self.authorizations[request.accessToken]:
                return iot_service_pb2.TemperatureReply(status="Ok", temperature=current_temperatures[request.sensorName])
            else:
                return iot_service_pb2.TemperatureReply(status="Erro de autorização", temperature="")
        else:
            return iot_service_pb2.TemperatureReply(status="Erro de identificação", temperature="")

    def BlinkLed(self, request, context):
        if request.accessToken in self.authorizations:
            if request.sensorName in self.authorizations[request.accessToken]:
                ledName = request.sensorName.split('-')[1]
                produce_led_command(request.state, ledName)
                led_state[ledName] = request.state
                return iot_service_pb2.LedReply(status="Ok", ledstate=led_state)
            else:
                return iot_service_pb2.LedReply(status="Erro de autorização", ledstate={})
        else:
            return iot_service_pb2.LedReply(status="Erro de identificação", ledstate={})
    
    def SayLuminosity(self, request, context):
        if request.accessToken in self.authorizations:
            if request.sensorName in self.authorizations[request.accessToken]:
                return iot_service_pb2.LuminosityReply(status="Ok", luminosity=current_luminosities[request.sensorName])
            else:
                return iot_service_pb2.LuminosityReply(status="Erro de autorização", luminosity="")
        else:
            return iot_service_pb2.LuminosityReply(status="Erro de identificação", luminosity="")


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    iot_service_pb2_grpc.add_IoTServiceServicer_to_server(IoTServer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()

    temperatureTrd = threading.Thread(target=consume_temperature)
    temperatureTrd.start()

    luminosityTrd = threading.Thread(target=consume_luminosity)
    luminosityTrd.start()

    # Initialize the state of the leds on the actual device
    for color in led_state.keys():
        produce_led_command(led_state[color], color)
    serve()
