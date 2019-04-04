from paho.mqtt.client import Client
from multiprocessing import Process
from multiprocessing import Lock
from multiprocessing import Array
import time, random

class Seller:
    '''
    Set objects for sale and publish them on 'Available-items' topic
    '''
    def __init__(self, number_items, broker = 'localhost', auth = None):
        self.number_of_items = number_items
        self.auth = auth
        self.client = Client()
        
        if auth != None:
            (usr, pwd) = auth
            self.client.username_pw_set(usr, pwd)
            
        self.client.connect(broker)

    def sell_process(self, update = False):
        available_itms = ''.join([str(x)+' ' for x in
                                  range(1, self.number_of_items + 1)])
        self.client.publish('Available-items', available_itms)
        while update:
            self.client.publish('Available-items', available_itms)
            time.sleep(3*random.random())

    def sell(self):
        Process(target = self.sell_process, args = ()).start()



if __name__ == '__main__':

    seller = Seller(3, 'localhost', auth = ("seller", "sellerpassword"))
    seller.sell()

