
#!/usr/bin/env python3
import time
#from serial import Serial
import serial
from paho.mqtt import client as mqtt_client

ser = serial.Serial( port='/dev/ttyUSB0',
                        baudrate = 9600,
                        parity=serial.PARITY_NONE,
                        stopbits=serial.STOPBITS_ONE,
                        bytesize=serial.EIGHTBITS,
                        timeout=1)

while 1:
        x=ser.readline()
        print (x),

#!/usr/bin/env python3
import time
#from serial import Serial
import serial
from paho.mqtt import client as mqtt_client

ser = serial.Serial( port='/dev/ttyUSB0',
                        baudrate = 9600,
                        parity=serial.PARITY_NONE,
                        stopbits=serial.STOPBITS_ONE,
                        bytesize=serial.EIGHTBITS,
                        timeout=1)

while 1:
        x=ser.readline()
        print (x),