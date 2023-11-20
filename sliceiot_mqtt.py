import paho.mqtt.subscribe as subscribe
import paho.mqtt.client as mqtt 
import sqlite3
import json
import base64
import random
import time
import sys
import re

# HOST = '139.59.41.218'
# KEEPALIVE = 600 
#topic = 'application/+/device/+/+'


#topic = 'application/81d483fc-a393-478e-9c84-5329870ec3ae/device/+/event/+'
#tenants/00000000-0000-0000-0000-000000000002/applications/81d483fc-a393-478e-9c84-5329870ec3ae/devices/9ab976002d032c4c/events
msg="1,4.34,5.99,404,404"
#def on_message(client, userdata, msg):

#     msg = subscribe.simple(topic, hostname=HOST)
# 
#     payload = msg.payload
#     print(payload)
#     string = payload.decode('utf-8')
# 
#     newdata = json.loads(string)
#     
#     meterdata = newdata['data']
#     print(meterdata)
#     output = base64.b64decode(meterdata)
#     
#     output = output.decode()
#     print(output)



#output="1,4.34,5.99,404,404"
SliceIoT_HOST = '139.59.73.240'
    #The access token is a uniq identity to the device created inside the SliceIoT server
ACCESS_TOKEN = 'Dd8BVksDUzRf6nAM5Yqo'  #//iitm
    #ACCESS_TOKEN='ie27wbIacXcKVA9HFfBX'    #//iit rnu
    #ACCESS_TOKEN='A0FavFONiySYS75652kF'     #//iit rnu jr
client = mqtt.Client()
    #The access token is used as username and password in MQTT
client.username_pw_set(ACCESS_TOKEN)
    #Connect to SliceIoT using default MQTT port and 10 seconds keepalive interval
client.connect(SliceIoT_HOST, 1883, 10)
client.loop_start()
while True:
    output="1,{},5.99,404,404".format(random.randrange(4, 20)) 
    oc=output.split(",")
    gateway_data = {"Node id":oc[0],"Ch1":oc[1],"Ch2":oc[2],"Ch3":oc[3],"Ch4":oc[4]}
    #gateway_data = {"Node id":output[0],"Ch1":output[1],"Ch2":output[2],"Ch3":output[3],"Ch4":output[4]}
    #"1,4.34,5.99,404,404"
   
    #"client.publish" is used in order to publish telemetry data to SliceIoT server
    #All data are sent to the topic id:'v1/devices/me/telemetry'
    client.publish('v1/devices/me/telemetry', json.dumps(gateway_data))
    #client.publish('v1/devices/me/telemetry', json.dumps(gateway_data1))

    #print ("sending data : \n ")
    print (gateway_data)
    time.sleep(10)
    #"json.dumps" is used to convert dictionary valuse to a string
client.loop_stop()
client.disconnect()

#subscribe.callback(on_message, topic, hostname=HOST, keepalive=KEEPALIVE)




    
    



































