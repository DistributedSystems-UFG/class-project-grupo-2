import threading
from concurrent import futures
from random import shuffle
import logging
import pickle
import uuid
from const import *
from kafka import KafkaConsumer, KafkaProducer
import grpc
import iot_service_pb2
import iot_service_pb2_grpc

# A in-memory DB of user
usersDB = {}

# A in-memory DB of access tokens
accessTokenDB = {}

# A in-memory DB of authorizations
authorizationsDB = {}

def new_token():
    return str(uuid.uuid4())

def new_user(login, password, auths):
    token = new_token()
    usersDB[login] = password
    accessTokenDB[login] = token
    authorizationsDB[token] = auths

# Create the default users
new_user('Alice', '123456', ['lavanderia', 'sala', 'banheiro'])
new_user('Bob', 'qwert', ['cozinha', 'escritorio', 'quarto'])

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
    # usersDB = {"Alice": "123456", "Bob": "qwert"}
    # accessToken = {
    #     "Alice": "69ace8a2-96a6-11ed-a1eb-0242ac120002",
    #     "Bob": "73a25f82-96aa-11ed-a1eb-0242ac120002",
    # }
    # authorizations = {
    #     # lavanderia, sala, cozinha, escritório, quarto, banheiro
    #     "69ace8a2-96a6-11ed-a1eb-0242ac120002": ['lavanderia', 'sala', 'banheiro'],
    #     "73a25f82-96aa-11ed-a1eb-0242ac120002": ['cozinha', 'escritorio', 'quarto']
    # }

    def AddNewUser(self, request, context):
        regions = ['lavanderia', 'sala', 'banheiro', 'cozinha', 'escritorio', 'quarto']
        login = request.login
        password = request.password

        new_user(login, password, shuffle(regions)[:3])
        
        return iot_service_pb2.AddNewUserReply(status="Ok")

    def GetAccessToken(self, request, context):
        login = request.login
        password = request.password
        accessGranted = False
        if login in usersDB:
            if usersDB[login] == password:
                accessGranted = True

        if accessGranted:
            token = accessTokenDB[login]
            return iot_service_pb2.Token(status="acesso concedido", token=token)
        else:
            return iot_service_pb2.Token(status="acesso negado")
    
    def GetRegions(self, request, context):
        if request.accessToken in authorizationsDB:
            list = iot_service_pb2.Regions(status="Ok")
            for region in authorizationsDB[request.accessToken]:
                list.regions.append(iot_service_pb2.Region(
                    name=region,
                    icon="icone-"+region,
                ))

            return list
        else:
            return iot_service_pb2.Regions(status="Erro de identificação")
    
    def AddRegion(self, request, context):
        if request.accessToken in authorizationsDB:
            region = request.region.name
            authorizationsDB[request.accessToken].append(region)
            return iot_service_pb2.AddRegionReply(status="Ok")
        else:
            return iot_service_pb2.AddRegionReply(status="Erro de identificação")
    
    def RemoveRegion(self, request, context):
        if request.accessToken in authorizationsDB:
            region = request.region.name
            if region in authorizationsDB[request.accessToken]:
                authorizationsDB[request.accessToken].remove(region)
                return iot_service_pb2.RemoveRegionReply(status="Ok")
        else:
            return iot_service_pb2.RemoveRegionReply(status="Erro de identificação")
    
    def GetLastRoute(self, request, context):
        if request.accessToken in authorizationsDB:
            pass
        else:
            return iot_service_pb2.RouteReply(status="Erro de identificação")
    
    def SetRoute(self, request, context):
        if request.accessToken in authorizationsDB:
            pass
        else:
            return iot_service_pb2.SetRouteReply(status="Erro de identificação")

    def SayTemperature(self, request, context):
        if request.accessToken in authorizationsDB:
            if request.sensorName in authorizationsDB[request.accessToken]:
                return iot_service_pb2.TemperatureReply(status="Ok", temperature=current_temperatures[request.sensorName])
            else:
                return iot_service_pb2.TemperatureReply(status="Erro de autorização")
        else:
            return iot_service_pb2.TemperatureReply(status="Erro de identificação")

    def BlinkLed(self, request, context):
        if request.accessToken in authorizationsDB:
            if request.sensorName in authorizationsDB[request.accessToken]:
                ledName = request.sensorName.split('-')[1]
                produce_led_command(request.state, ledName)
                led_state[request.sensorName] = request.state
                return iot_service_pb2.LedReply(status="Ok", ledstate=led_state)
            else:
                return iot_service_pb2.LedReply(status="Erro de autorização")
        else:
            return iot_service_pb2.LedReply(status="Erro de identificação")
    
    def SayLuminosity(self, request, context):
        if request.accessToken in authorizationsDB:
            if request.sensorName in authorizationsDB[request.accessToken]:
                return iot_service_pb2.LuminosityReply(status="Ok", luminosity=current_luminosities[request.sensorName])
            else:
                return iot_service_pb2.LuminosityReply(status="Erro de autorização")
        else:
            return iot_service_pb2.LuminosityReply(status="Erro de identificação")


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
