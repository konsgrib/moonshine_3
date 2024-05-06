import pika
import json
from time import sleep

import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
from factory import Factory

factory = Factory()
t1 = factory.create_device("TempertureSensor",device_id="28-42f7d445552f")
t2 = factory.create_device("TempertureSensor",device_id="28-5be6d445359c")
h = factory.create_device("HumidityLevelSensor",pin=14)
relay_pwr = factory.create_device("Relay",pin=19)
relay_clr = factory.create_device("Relay",pin=13)
relay_v1 = factory.create_device("Relay",pin=6)
relay_v2 = factory.create_device("Relay",pin=5)
messenger = factory.create_device("MessengerFile",filename="state.txt")




while True:
    sleep(1)
    values = {
        "sensor1": t1.get_value().value,
        "sensor2": t2.get_value().value,
        "sensor3": h.get_value().value,
        "device1": relay_pwr.get_value().value,
        "device2": relay_clr.get_value().value,
        "device3": relay_v1.get_value().value,
        "device4": relay_v2.get_value().value,
        "message": messenger.get_message(),
    }
    credentials = pika.PlainCredentials('pi','Pi#2024')
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost',credentials=credentials))
    channel = connection.channel()
    channel.exchange_declare(exchange='logs', exchange_type='fanout')
    message = json.dumps(values)
    channel.basic_publish(exchange='logs', routing_key='', body=message)
    print(f" [x] Sent {message}")
    connection.close()
