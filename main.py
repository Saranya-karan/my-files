#My main program
import time
import machine
import network
import ujson
import ubinascii
from simple1 import MQTTClient
from fetch_credentials import credentials_dict

SSID = credentials_dict.get('wifi_ssid', '')
PASS = credentials_dict.get('wifi_password', '')
CLIENT_ID = credentials_dict.get('client_id', '')
AWS_ENDPOINT = credentials_dict.get('aws_endpoint', '')
PUB_TOPIC = credentials_dict.get('pub_topic', '')
SUB_TOPIC = credentials_dict.get('sub_topic', '')


def read_cert(filename):
    try:   
        with open(filename, 'r') as f:
            # print(f.read())
            text = f.read().strip()
            split_text = text.split('\n')
            base64_text = ''.join(split_text[1:-1])
            # Decode base64-encoded data, ignoring invalid characters in the input. Conforms to RFC 2045 s.6.8. Returns a bytes object.
            return ubinascii.a2b_base64(base64_text)
    except Exception as e:
        raise e


DEV_KEY = read_cert('credentials/private.pem.key')
DEV_CRT = read_cert('credentials/certificate.pem.crt')
light = machine.Pin("LED", machine.Pin.OUT)
light.off()

def wifi_connect():
    print('Connecting to wifi...')
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID, PASS)
    while wlan.isconnected() == False:
        light.on()
        print('Waiting for connection...')
        time.sleep(0.5)
        light.off()
        time.sleep(0.5)
    print('Connection details: %s' % str(wlan.ifconfig()))

# Callback function for all subscriptions
def mqtt_subscribe_callback(topic, msg):
    print("Received topic: %s message: %s" % (topic, msg))
    if topic == SUB_TOPIC:
        mesg = ujson.loads(msg)
        if 'state' in mesg.keys():
            if mesg['state'] == 'on' or mesg['state'] == 'ON' or mesg['state'] == 'On':
                light.on()
                print('Light is ON')
            else:
                light.off()
                print('Light is OFF')

def get_rpi_temperature():
    sensor = machine.ADC(4)
    voltage = sensor.read_u16() * (3.3 / 65535)
    temperature = 27 - (voltage - 0.706) / 0.001721
    return temperature

wifi_connect()

mqtt = MQTTClient(
    client_id=CLIENT_ID,
    server=AWS_ENDPOINT,
    port=8883,
    keepalive=120,
    ssl=True,
    ssl_params={'key':DEV_KEY, 'cert':DEV_CRT, 'server_side':False})

mqtt.connect()
mqtt.set_callback(mqtt_subscribe_callback)

mqtt.subscribe(SUB_TOPIC)

while True:
    message = b'{"temperature":%s, "temperature_unit":"Degrees Celsius"}' % get_rpi_temperature()
    print('Publishing topic %s message %s' % (PUB_TOPIC, message))
    mqtt.publish(topic=PUB_TOPIC, msg=message, qos=1)
    mqtt.check_msg()
    time.sleep(5)