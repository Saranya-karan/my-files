import time
import machine
import network
import ujson
from simple1 import MQTTClient
import ubinascii
SSID = b'EagleEye'
PASS = b'8122266766'
CLIENT_ID = 'RaspberryPiPicoW'
AWS_ENDPOINT = 'a2s8fj8scmsaqi-ats.iot.us-east-1.amazonaws.com'
SUBSCRIBED_CHANNEL = 'led'
PUB_TOPIC = b'temperature'
SUB_TOPIC = b'temperature'

# with open('/pri.der', 'rb') as f:
#     DEV_KEY = f.read()
# with open('/cert.der', 'rb') as f:
#     DEV_CRT = f.read()
# import ubinascii
# 
def read_cert(filename):        
    with open(filename, 'r') as f:
        text = f.read().strip()
        split_text = text.split(b'\n')  # Split using bytes newline
        base64_text = b''.join(split_text[1:-1])  # Join the byte strings
        return ubinascii.a2b_base64(base64_text)

DEV_KEY = read_cert('/d5126a8b49f0e6423dd6f5129d8a493feaf53fbf393e3355d3532ca988a51978-private.pem.key')
DEV_CRT = read_cert('/d5126a8b49f0e6423dd6f5129d8a493feaf53fbf393e3355d3532ca988a51978-certificate.pem.crt')
# Define onboard LED and set its default state to off
light = machine.Pin("LED", machine.Pin.OUT)
light.off()

# Wifi Connection Setup
def wifi_connect():
    print('Connecting to wifi...')
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID, PASS)
    while not wlan.isconnected():
        light.on()
        print('Waiting for connection...')
        time.sleep(0.5)
        light.off()
        time.sleep(0.5)
    print('Connection details:', wlan.ifconfig())

# Callback function for subscriptions
def mqtt_subscribe_callback(topic, msg):
    print("Received topic: %s message: %s" % (topic, msg))
    if topic == SUB_TOPIC:
        mesg = ujson.loads(msg)
        if mesg.get('state') in ['on', 'ON', 'On']:
            light.on()
            print('Light is ON')
        else:
            light.off()
            print('Light is OFF')

# Read current temperature from RP2040 embedded sensor
def get_rpi_temperature():
    sensor = machine.ADC(4)
    voltage = sensor.read_u16() * (3.3 / 65535)
    temperature = 27 - (voltage - 0.706) / 0.001721
    return temperature

# Connect to wifi
wifi_connect()
# Set AWS IoT Core connection details
mqtt = MQTTClient(
    client_id=CLIENT_ID,
    server=AWS_ENDPOINT,
    port=8883,
    keepalive=10000,
    ssl=True,
    ssl_params={'key': DEV_KEY, 'cert': DEV_CRT, 'server_side': False}
)

# Establish connection to AWS IoT Core
mqtt.connect()

# Set callback for subscriptions
mqtt.set_callback(mqtt_subscribe_callback)

# Subscribe to topic
mqtt.subscribe(SUB_TOPIC)
PUB_TOPIC = "led"

# Main loop - with 5 sec delay
while True:
    # Publish the temperature
    message = b'{"temperature": %s, "temperature_unit": "Degrees Celsius"}' % get_rpi_temperature()
    print('Publishing topic %s message %s' % (PUB_TOPIC, message))
    mqtt.publish(topic=PUB_TOPIC, msg=message, qos=1)

    # Check subscriptions for messages
    mqtt.check_msg()
    time.sleep(5)

