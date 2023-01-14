import threading
import time

from kafka import KafkaProducer, KafkaConsumer

from const import *


def read_temp():
    temp_c = 25.0
    temp_f = temp_c * 9.0 / 5.0 + 32.0

    return temp_c, temp_f


def consume_led_command():
    consumer = KafkaConsumer(bootstrap_servers=KAFKA_SERVER + ':' + KAFKA_PORT)
    consumer.subscribe(topics=('ledcommand'))

    for msg in consumer:
        print('Led command received: ', msg.value)
        print('Led to blink: ', msg.key)

consumerThread = threading.Thread(target=consume_led_command)
consumerThread.start()

producer = KafkaProducer(bootstrap_servers=KAFKA_SERVER + ':' + KAFKA_PORT)
last_reported = 0

while True:
    (temp_c, temp_f) = read_temp()
    print(temp_c, temp_f)
    producer.send('temperature', str(temp_c).encode())
    time.sleep(1)
