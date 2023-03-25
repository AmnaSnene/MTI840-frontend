from flask import Flask, request, jsonify, render_template
import paho.mqtt.client as mqtt
import ssl
import threading
import ast
app = Flask(__name__)

# intialisation
temp, max_temp = 0, 0
ingredient = ''


@app.route('/')
def index():
    return render_template('index.html', temp=temp, max_temp=max_temp, ingredient=ingredient)

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))


client = mqtt.Client()
client.on_connect = on_connect
client.tls_set(ca_certs='./mti840-frontend/AmazonRootCA1.pem',
               certfile='./mti840-frontend/79463ac588a3d48b8b07746f94ab5a7bccc39f9b370d2b058ed02b88d6d16b74-certificate.pem.crt',
               keyfile='./mti840-frontend/79463ac588a3d48b8b07746f94ab5a7bccc39f9b370d2b058ed02b88d6d16b74-private.pem.key',
               tls_version=ssl.PROTOCOL_SSLv23)
client.tls_insecure_set(True)
client.connect("api.amazonaws.com", 8883,60)  # Taken from REST API endpoint - Use your own.


def subscribe(Dummy):
    def on_message(client, userdata, msg):
        """
            The callback function.
            """
        if msg.topic == "device/temp_cloud/ml":
            global ingredient
            #ingredient = msg.payload.decode()[1:-2].split(',')
            ingredient = ast.literal_eval(msg.payload.decode())
        else:
            global temp
            temp = ast.literal_eval(msg.payload.decode())["temperature"]
        print(f"{client} Received from `{msg.topic}` topic")
        print("received")

    def on_subscribe(client, userdata, mid, granted_qos):
        print(f"Subscribed{client._client_id.decode()}")

    client.on_subscribe = on_subscribe
    subscription_list = [("device/temp_cloud/ml",0), ("device/temp/data",0)]
    client.subscribe(subscription_list)
    client.on_message = on_message
    client.loop_forever()


threading.Thread(target=subscribe, args=("Create intrusion Thread",),).start()

if __name__ == '__main__':
    app.run()
