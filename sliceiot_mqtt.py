import paho.mqtt.subscribe as subscribe
import paho.mqtt.client as mqtt 
import sqlite3
import json
import base64
import random
import time
import sys
import re

HOST = '139.59.41.218'
KEEPALIVE = 600 
#topic = 'application/+/device/+/+'

topic = 'application/9619ca6c-887c-48f6-ba1e-b06cfe22f1dc/device/+/event/up'
#applications/81d483fc-a393-478e-9c84-5329870ec3ae/device/+/event/

def on_message(client, userdata, msg):

    msg = subscribe.simple(topic, hostname=HOST)

    payload = msg.payload
    print(payload)
    string = payload.decode('utf-8')

    newdata = json.loads(string)
    
    meterdata = newdata['data']
    print(meterdata)
    output = base64.b64decode(meterdata)
    
    output = output.decode()
    print(output)
   ############################
    SliceIoT_HOST = '139.59.73.240'

    ACCESS_TOKEN = '2R4vmgDf5AzbI0WOJHIu'  #//iitm


    client = mqtt.Client()

    client.username_pw_set(ACCESS_TOKEN)

    client.connect(SliceIoT_HOST, 1883, 10)
    client.loop_start()
    
    oc=output.split(",")
    gateway_data = {"Node id":oc[0],"Ch1":oc[1],"Ch2":oc[2],"Ch3":oc[3],"Ch4":oc[4]}

    client.publish('v1/devices/me/telemetry', json.dumps(gateway_data))

    time.sleep(0.5)

    print (gateway_data)

    client.loop_stop()
    client.disconnect()

subscribe.callback(on_message, topic, hostname=HOST, keepalive=KEEPALIVE)



    
    





































    
    



































