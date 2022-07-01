import paho.mqtt.client as mqtt


class MQTTConfig(mqtt.Client):
    def __init__(self):
        super().__init__()
        # self.username_pw_set('username', 'password')
