import paho.mqtt.client as mqtt
import ssl
import json

CA = 'certificates\\AmazonRootCA1.pem'
CERTI = 'certificates\\6fcbc80f7e-certificate.pem.crt'
KEYFILE = 'certificates\\6fcbc80f7e-private.pem.key'

def on_connect(c, u, f, rc):
  print("resource code" + str(rc))
  mqtt.subscribe("waves22", 0)

def on_message(c , u, msg):
  data =(msg.payload).decode("utf-8")
  data = data.replace("\'", "\"")
  data = json.loads(data)
  print(data)

  beachname = data['BeachName']
  temperature = round(float(data['WaterTemperature']),3)
  turbidity=round(float(data['Turbidity']),3)
  waveperiod=round(float(data['WavePeriod']),3)
  waveheight=round(float(data['WaveHeight']),3)
  if(float(temperature) > 0 and float(turbidity) > 0 and float(waveheight) >0 and float(waveperiod) >0):
    file2 = open("data.txt","r")
    x = file2.readlines()
    file2.close()
    file3 = open("data.txt","a")
    for i in range(len(x)):
        z=x[i].split(',')
        print(z[0]== str(beachname))
        if(z[0] == str(beachname)):
          del x[i]
          break
    open('data.txt', 'w').close()      
    for line in x:
      file3.write(line)     
          
    file3.close()
    file2.close()
    
    
    
    file1 = open("data.txt","a")
      
    file1.write(str(beachname)+','+str(temperature)+','+str(turbidity)+','+str(waveperiod)+','+str(waveheight)+'\n')
  else:
    return
  
mqtt = mqtt.Client()
mqtt.tls_set(CA, CERTI, KEYFILE, cert_reqs = ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1_2, ciphers = None)
mqtt.connect("a38atymf8oln79-ats.iot.us-east-1.amazonaws.com", 8883, 60)

mqtt.on_connect = on_connect
mqtt.on_message = on_message
mqtt.loop_forever()
