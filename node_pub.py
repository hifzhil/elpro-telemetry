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
                      "/evos_telemetry/temp"]
        self.rpm_ = 1000
        self.speed_ = 38
        self.temp_ = 76
        self.messages = ["40", "1800", "76"]
        self.client_id = f'publish-{random.randint(0, 1000)}'
        # self.username = 'emqx'
        # self.password = 'public'

        ## reading serial stuff
        # self.ser_ = serial.Serial( port='/dev/ttyUSB0',
        #                 baudrate = 9600,
        #                 parity=serial.PARITY_NONE,
        #                 stopbits=serial.STOPBITS_ONE,
        #                 bytesize=serial.EIGHTBITS,
        #                 timeout=1)
    
    def connect_to_mqtt(self) -> mqtt_client:
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


    def publisher(self, client):
        msg_count = 1
        while True:
            time.sleep(1)
            self.speed_callback()
            self.rpm_callback()
            self.temp_callback()

            for topic, msg in zip(self.topics, self.messages) :
                result = client.publish(topic, str(int(msg)+1))
                # result: [0, 1]
                status = result[0]
                if status == 0:
                    print(f"Send `{msg}` to topic `{topic}`")
                else:
                    print(f"Failed to send message to topic {topic}")
            msg_count += 1
            if msg_count > 1000:
                break

    def speed_callback(self):
        a = int(self.messages[0])
        a +=1 
        self.messages[0] = str(a)
    
    def rpm_callback(self):
        a = int(self.messages[1])
        a +=1 
        self.messages[1] = str(a)
    
    def temp_callback(self):
        a = int(self.messages[2])
        a +=1 
        self.messages[2] = str(a)
    
    
    def update(self):
        # x=self.ser_.readline()
        # print (x),
        client = self.connect_to_mqtt()
        client.loop_start()
        self.publisher(client)
        client.loop_stop()
        

def main():
    try :
        evos_pub=Telemetry()
        evos_pub.update()
    except KeyboardInterrupt:
        print("Shutting down")

if __name__ == '__main__':
    try :
        main()
    except NameError:
      print("memory leaks, check your class variable")
