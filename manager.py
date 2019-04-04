from paho.mqtt.client import Client
from multiprocessing import Process
from multiprocessing import Lock
from multiprocessing import Array
import time, random

class Judge:

    max_time = 0
    elapsed_time = 0
    initial_time = 0
    lock = Lock()
    lst = []                          # List of available objects
    lst_results = Array('i', 0)       # Max value for each object
    lst_names = []                    # Name of winner for each object
    
    def __init__(self, max_timeout, broker = 'localhost', auth = None):
        self.max_time = max_timeout
        self.auth = auth
        self.client = Client()
        
        if auth != None:
            (usr, pwd) = auth
            self.client.username_pw_set(usr, pwd)
            
        self.client.connect(broker)        
        

    def on_message(self, client, userdata, msg):
        if msg.topic == 'Available-items':
            '''
            This msg contains all available objects. Once received, 
            update the self list to contain them, then create the
            results list for keeping maximum value for each object.
            '''
            self.lst = msg.payload
            self.lst = self.lst.decode("utf-8")
            self.lst = list(map(int, self.lst.split()))
            self.lst_results = Array('i', len(msg.payload))

            print('Available objects', self.lst)
            
            for i in range(len(self.lst)):
                self.lst_names.append('')

            Process(target = self.collect, args = ()).start()
            time.sleep(2*random.random())
            
            for i in range(1, len(self.lst) + 1): 
                self.client.publish('results/' + str(i),
                                    str(0) + ' ' + str('None'))
                
            self.initial_time = time.time()
            self.elapsed_time = time.time() - self.initial_time

        else:
            with self.lock:
                time.sleep(random.random())
                self.elapsed_time = time.time() - self.initial_time
                if self.elapsed_time < self.max_time:
                    self.update_value(msg)
                else:
                    if len(self.lst_names) != 0:
                        print('Timeout reached, no more bids are accepted')

                        for i in self.lst:
                            top = 'results/' + str(i)
                            own = str(self.lst_names[i - 1])
                            client.publish(top, 'Winner is ' + own)
                            
                        self.client.unsubscribe('items/#')
                    self.lst_names = []
           

    def update_value(self, msg):
        '''
        Manage every msg received: 
            1- update the current value for each object (mutex with self.lock)
            2- publish the value in the corresponding topic
        '''
        item_topic = msg.topic
        (rest, bid_owner) = msg.payload.decode("utf-8").split()
        result_topic = item_topic.replace('items', 'results')
        item_pos = int(item_topic.replace('items/', '')) - 1       
        item_value = int(rest)        
        last_value = self.lst_results[item_pos]
        
        self.lst_results[item_pos] = max(last_value, item_value)
        self.lst_names[item_pos] = str(bid_owner)
        
        current_value = self.lst_results[item_pos]
                
        self.client.publish(result_topic,
                            str(current_value) + ' ' + str(bid_owner))
        print('New winner for',
              str(msg.topic).replace('items/', 'item '),
              ':', bid_owner)


    def self_process(self, topic):        
        self.client.subscribe('items/' + str(topic))
        self.client.on_message = self.on_message
        self.client.loop_forever()

    def collect(self):        
        print('Waitting users to bid ...')
        
        for it in self.lst:
            self.client.subscribe('items/' + str(it))
            
        self.client.on_message = self.on_message
        self.client.loop_forever()

    def get_items(self):
        self.client.subscribe('Available-items')
        self.client.on_message = self.on_message
        self.client.loop_forever()
        
    def start(self):
        self.get_items()

    
if __name__ == '__main__':
    BROKER = 'localhost'
   
    manager = Judge(60, BROKER, auth = ("manager", "managerpassword"))
    manager.start()
    

    
    



