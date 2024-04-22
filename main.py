from utils import decrypt_data
from node_publisher import Telemetry
from node_serial import SerialData
import time
import threading
from collections import namedtuple
# from data_parameter import Parameters

class Parameters:
    def __init__(self, rpm, speed, temperature, limiter):
        self.rpm = rpm
        self.speed = speed
        self.temperature = temperature
        self.limiter = limiter

evos_param = Parameters(rpm=0, speed=0, temperature=0, limiter=0)
evos_pub=Telemetry()
mcu_serial = SerialData()

def first_core():
    global evos_param
    try :
        while True:
            
            evos_pub.rpm_callback(evos_param.rpm)
            evos_pub.speed_callback(evos_param.speed)
            evos_pub.temp_callback(evos_param.temperature)
            evos_pub.lim_callback(evos_param.limiter)

            evos_pub.update()
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("core 1 down")

def second_core():
    global evos_param
    try:
        while True:
            mcu_serial.update()
            mcu_data = mcu_serial.get_data()
            raw_data = decrypt_data(mcu_data)
            print(raw_data)
            evos_param = Parameters(*raw_data)
    except KeyboardInterrupt:
        print("core 2 down")
        
def main():
    try :
        evos_pub.connect_to_mqtt()
        time.sleep(0.5)

        core1 = threading.Thread(target=first_core)
        core2 = threading.Thread(target=second_core)

        
        core1.start()
        core2.start()

        core1.join()
        core2.join()

    except KeyboardInterrupt:
        print("Shutting down")
    except Exception as e:
        print("An error occurred:", e)


if __name__ == '__main__':
    try :
        main()
    except NameError:
      print("memory leaks, check your class variable")
