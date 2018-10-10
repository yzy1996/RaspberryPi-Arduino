import paho.mqtt.client as mqtt
import numpy as np
from PIL import Image
import tensorflow as tf
from tensorflow.python.keras.models import load_model


TEMP_FILE = './tmp/temp.jpg'
cat_dict = {0:'Munchkins', 1:'Ocelot', 2:'Singapura', 3:'Turkish_Van'}
host_name = 'team11.sws3009.bid'

graph = tf.get_default_graph()
model_file = 'cat.hd5'

auth = {'username':'icy', 'password':'iceice000'}


def load_image(image_name):
    image = Image.open(image_name)
    image = image.resize((249, 249))
    image_array = np.array(image) / 255.
    return np.expand_dims(image_array, axis=0)


def classify(model, image_array, cat_dict):
    global graph
    with graph.as_default():
        result = model.predict(image_array)
        index = np.argmax(result)
    return cat_dict[index], result[0][index], index


def on_connect(client, userdata, flags ,rc):
    print("Connect with result code:{}".format(rc))
    client.subscribe("IMAGE/classify")


def on_message(client, userdata, msg):
    img = msg.payload

    #write to temp file

    with open(TEMP_FILE, 'wb') as f:
        f.write(img)

    img_array = load_image(TEMP_FILE)

    label, prob, index = classify(model=model, image_array=img_array, cat_dict=cat_dict)

    print("classified as {} with certainty {}".format(label, prob))

    client.publish("IMAGE/predict", '{}:{}:{}'.format(label, prob, index))


def setup(host_name):
    global client
    client = mqtt.Client()
    client.username_pw_set(auth['username'], auth['password'])
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(host_name)
    client.loop_start()


def main():
    global model
    model = load_model(model_file)
    setup(host_name=host_name)
    while True:
        pass


if __name__ == '__main__':
    main()

