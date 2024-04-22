#!/usr/bin/env python3

import random
import time
import serial
from paho.mqtt import client as mqtt_client


class Telemetry(object):
    def __init__(self) : 
        # mqtt stuff, this is common variable on whatever broker u use
        self.broker = 'broker.emqx.io'
        self.port = 1883
        self.topics= ["/evos_telemetry/speed",
                      "/evos_telemetry/rpm",
                      "/evos_telemetry/temp",
                      "/evos_telemetry/limiter"]
        self.rpm_ = 1000
        self.speed_ = 27
        self.temp_ = 76
        self.limiter_ = 38
        self.messages = ["38", 
                         "1800", 
                         "76", 
                         "38"]
        
        self.client_id = f'publish-{random.randint(0, 1000)}'
        # self.username = 'emqx'
        # self.password = 'public'
    
    def connect_to_mqtt(self) -> mqtt_client:
        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                print("Connected to MQTT Broker!")
            else:
                print("Failed to connect, return code %d\n", rc)

        self.evo_client = mqtt_client.Client(self.client_id)
        # self.evo_client = mqtt_client.Client(mqtt_client.CallbackAPIVersion.VERSION1, self.client_id)
        self.evo_client.on_connect = on_connect
        self.evo_client.connect(self.broker, self.port)

    def publisher(self, client):
        for topic, msg in zip(self.topics, self.messages) :
            result = client.publish(topic, msg)
            # result: [0, 1]
            status = result[0]
            # if status == 0:
                # print(f"Send `{msg}` to topic `{topic}`")
            # else:
                # print(f"Failed to send message to topic {topic}")

    def speed_callback(self, speed):
        self.messages[0] = str(speed)
    
    def rpm_callback(self, rpm):
        self.messages[1] = str(rpm)
    
    def temp_callback(self, temp):
        self.messages[2] = str(temp)
        
    def lim_callback(self, lim):
        self.messages[3] = str(lim)
    
    def update(self):
        # x=self.ser_.readline()
        # print (x),
        self.evo_client.loop_start()
        self.publisher(self.evo_client)
        self.evo_client.loop_stop()
