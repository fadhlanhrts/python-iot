from flask import Flask, render_template
from flask_mqtt import Mqtt

app = Flask(__name__)
app.config['MQTT_BROKER_URL'] = '192.168.1.134'
app.config['MQTT_BROKER_PORT'] = 1883
app.config['MQTT_USERNAME'] = 'admin'
app.config['MQTT_PASSWORD'] = 'admin'
app.config['MQTT_KEEPALIVE'] = 5
app.config['MQTT_TLS_ENABLED'] = False
mqtt = Mqtt(app)


@mqtt.on_connect()
def handle_connect_temp(client, userdata, flags, rc):
    mqtt.subscribe('home/livingroom/temperature')
    mqtt.subscribe('home/livingroom/humidity')


@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    
    print(message.topic)
    if message.topic == 'home/livingroom/temperature':
        print('Temp is', message.payload.decode('utf-8'))
    else:
        print('Humid is', message.payload.decode('utf-8'))
    
    #if message.payload.decode() <= 30.0:
      #  print('This is temp')

    data = dict(
        topic=message.topic,
        payload=message.payload.decode()
    )


@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)