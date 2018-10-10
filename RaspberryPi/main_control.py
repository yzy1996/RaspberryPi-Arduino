import serial #module for serial port communication
from pynput import keyboard
import paho.mqtt.client as mqtt
import time
import os



ser = serial.Serial('/dev/ttyS0', 9600, timeout=1)

flag = 0
#Note: Serial port read/write returns "byte" instead of "str" 
#ser.write("testing serial connection\n".encode('utf-8'))
#ser.write("sending via RPi\n".encode('utf-8'))





resp_callback = None
host_name = "team11.sws3009.bid"

auth = {'username':'icy', 'password':'iceice000'}
path = './capture/'



def setup(host_name):
    global client
    client = mqtt.Client()
    client.username_pw_set(auth['username'], auth['password'])
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(host_name)
    client.loop_start()


def on_connect(client, userdata, flag, rc):
    print("Connected with result code:{}".format(rc))
    client.subscribe("IMAGE/predict")


def on_message(client, userdata, msg):
    print('Received msg from server')
    received_str = msg.payload.decode('utf-8').split(':')
    resp_callback(received_str[0], float(received_str[1]), int(received_str[2]))

    # if resp_callback is not None:
    #     resp_callback(received_str[0], float(received_str[1]), int(received_str[2]))


def load_image(file_name):
    os.system('wget http://localhost:8080/?action=snapshot -O {}'.format(file_name))
    with open(file_name, 'rb') as f:
        data = f.read()
    return data


def send_image(file_name):
    img = load_image(file_name)
    client.publish("IMAGE/classify", img)


def resp_handler(label, prob, index):
    print("\n -- Response --\n\n")
    print("Label:{}".format(label))
    print("Probability:{}".format(prob))
    print("Index:{}".format(index))


def start_client():
    setup(host_name)
    global resp_callback
    # setup(host_name=host_name)
    resp_callback = resp_handler


def classify_image(image_name):
    print('Start uploading {}'.format(image_name))
    send_image(file_name=image_name)
    # time.sleep(1)





def on_press(key):
    try:
        if key.char == 'p':
            classify_image(path + '00{}.jpg'.format(0))
        #print('alphanumeric key  {0} pressed'.format(key.char))
        user = key.char + '\n'
        ser.write(user.encode('utf-8'))
		
    except AttributeError:
        print('special key {0} pressed'.format(key))

def on_release(key):
    #print('{0} released'.format(key))
    user = 'x' + '\n'
    ser.write(user.encode('utf-8'))
	
    if key == keyboard.Key.esc:
        return False

try:
    start_client() 
    while 1:
        if flag == 0:
            user1 = "hello"
            ser.write(user1.encode('utf-8'))
            response = ser.readline()
            print("connecting")
            user2 = "ack"
            if response.decode('utf-8') == "ack":
                ser.write(user2.encode('utf-8'))
                print("connecting ok!")
                flag = 1
                
        if flag == 1:
            with keyboard.Listener(
                on_press = on_press,
                on_release = on_release) as listener:
                listener.join()
            #user = input() + '\n'
            #ser.write(user.encode('utf-8'))
            
except KeyboardInterrupt:
    ser.close()


