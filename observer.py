from paho.mqtt.client import Client
from multiprocessing import Process
import sys, os

class Observer:
    '''
    Simple object to observe topics;
    used for testing cliente-manager-seller comunication
    '''
       
    def __init__(self, broker, auth = None):
        self.client = Client()
        if auth != None:
            (usr, pwd) = auth
            self.client.username_pw_set(usr, pwd)
        self.client.on_message = self.on_message
        self.client.connect(broker)
    
    def on_message(self, client, userdata, msg):
        print(msg.topic, msg.payload.decode("utf-8"))
    

    def start(self, topics):
        self.client.subscribe(topics)
        Process(target = self.client.loop_forever, args = ()).start()

if __name__ == '__main__':
    BROKER = 'localhost'
        
    observer = Observer(BROKER, auth = ("observer", "observerpassword"))   
    observer.start('results/#')
        


