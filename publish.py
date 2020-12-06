import ssl
import paho.mqtt.client as mqtt
from time import sleep
from random import choice
from random import seed
import os
import pandas as pd

CA = 'certificates\\AmazonRootCA1.pem'
CERTI = 'certificates\\6fcbc80f7e-certificate.pem.crt'
KEYFILE = 'certificates\\6fcbc80f7e-private.pem.key'

data = pd.read_csv("dataset/beach.csv")
info = data.loc[:, ["Beach Name", "Measurement Timestamp", "Water Temperature", "Turbidity", "Transducer Depth", "Wave Height", "Wave Period", "Battery Life", "Measurement Timestamp Label","Measurement ID"]]

mqtt = mqtt.Client()
mqtt.tls_set(CA, CERTI, KEYFILE, cert_reqs=ssl.CERT_REQUIRED,tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None)
mqtt.connect("a38atymf8oln79-ats.iot.us-east-1.amazonaws.com",8883, 60)
sleep(10)
mqtt.loop_start()
c = 0

def main():
    print('Starting...')
    for i in range(20000, 30000):
        try:
            dataToBeSent = """{
                    'BeachName' : '%s',
                    'MeasurementTimestamp' : '%s',
                    'WaterTemperature': '%s',
                    'Turbidity':'%s',
                    'TransducerDepth':'%s',
                    'WaveHeight':'%s',
                    'WavePeriod':'%s'
                }""" % (
                info.loc[i, 'Beach Name'],
                info.loc[i, 'Measurement Timestamp'],
                info.loc[i, 'Water Temperature'],
                info.loc[i, 'Turbidity'],
                info.loc[i, 'Transducer Depth'],
                info.loc[i, 'Wave Height'],
                info.loc[i, 'Wave Period'],
            )
            print(dataToBeSent)
            mqtt.publish("waves22",dataToBeSent)
            sleep(1)
        except:
            print('Exiting...')
            break
            mqtt.disconnect()
main()
