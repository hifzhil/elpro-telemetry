#!/usr/bin/env python3

import random

from paho.mqtt import client as mqtt_client


class Telemetry(object):
    def __init__(self) : 
        # mqtt stuff, this is common variable on whatever broker u use
        self.broker = 'broker.emqx.io'
        self.port = 1883
        self.topic_speed_ = "/evos_telemetry/speed"
        self.topic_rpm_ = "/evos_telemetry/rpm"
        self.topic_temp_ = "/evos_telemetry/temp"
        self.client_id = f'publish-{random.randint(0, 1000)}'
        # self.username = 'emqx'
        # self.password = 'public'    
    def connect_mqtt(self) -> mqtt_client:
        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                print("Connected to MQTT Broker!")
            else:
                print("Failed to connect, return code %d\n", rc)

        client = mqtt_client.Client(self.client_id)
        # client = mqtt_client.Client(mqtt_client.CallbackAPIVersion.VERSION1, client_id)
        # client.username_pw_set(username, password)
        client.on_connect = on_connect
        client.connect(self.broker, self.port)
        return client


    def subscriber(self, client: mqtt_client):
        def on_message(client, userdata, msg):
            print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")

        client.subscribe(self.topic_speed_)
        client.on_message = on_message


    def run(self):
        client = self.connect_mqtt()
        self.subscriber(client)
        client.loop_forever()


def main():
    try :
        evos_sub=Telemetry()
        evos_sub.run()
    except KeyboardInterrupt:
        print("Shutting down")

if __name__ == '__main__':
    try :
        main()
    except NameError:
      print("memory leaks, check your class variable")
