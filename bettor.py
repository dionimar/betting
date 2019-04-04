from paho.mqtt.client import Client
from multiprocessing import Process
from multiprocessing import Lock
import random, time


class Bettor:
   
    def __init__(self, name, money, broker = 'localhost', auth = None):
        self.name = name
        self.lock = Lock()
        self.money = money
        self.client = Client()
        self.interest_objects = []
        self.alive = True
        
        if auth != None:
            (usr, pwd) = auth
            self.client.username_pw_set(usr, pwd)
            
        self.client.connect(broker)
        
        
    def on_message(self, client, userdata, msg):      
        if msg.topic == 'Available-items':
            self.lst = msg.payload
            self.lst = self.lst.decode("utf-8").split()
            self.interesting_items()
            
        else:
            '''
            Manage bid in terms of available money.
            Mutual exclusion to ensure money limitations between all
            bid processes.
            '''
            (current_bet,bid_owner) = msg.payload.decode("utf-8").split()
            current_bet=int(current_bet)
            
            if self.name != bid_owner:
                with self.lock:
                    if current_bet > self.money:
                        print('Limit reached for', self.name
                              , ' for item ', msg.topic.replace('results/', ''))
                        self.client.unsubscribe(msg.topic)
                        self.interest_objects.remove(msg.topic.replace('results/', ''))
                    else:
                        bet = current_bet + random.randint(1, 50)
                        topic = msg.topic.replace('results','items')
                        print(self.name, 'bets', bet, 'for', topic)
                        self.client.publish(topic, str(bet)
                                            + ' ' + str(self.name))
                        self.money -= bet

                                       
    def bet_process(self):
        self.client.on_message = self.on_message
        for it in self.interest_objects:
            self.client.subscribe('results/' + str(it))
        self.client.loop_forever()
        
            
    def interesting_items(self):
        n = random.randint(1, len(self.lst))
        self.interest_objects = random.sample(self.lst, n)
        print(self.name, 'will play for', self.interest_objects)
        Process(target = self.bet_process, args = ()).start()

            
    def get_items(self):
        self.client.subscribe('Available-items')
        self.client.on_message = self.on_message
        self.client.loop_forever()
        
           
    def start(self):
        Process(target = self.get_items, args = ()).start()
        
if __name__=='__main__':
    BROKER = 'localhost'
    
    bettor1 = Bettor(name = 'Alice', money = 1500,
                     broker = BROKER, auth = ("Alice", "Alicepassword"))
    bettor2 = Bettor(name = 'Bob', money = 2000,
                     broker = BROKER, auth = ("Bob", "Bobpassword"))
    bettor3 = Bettor(name = 'Marc', money = 1000,
                     broker = BROKER, auth = ("Marc", "Marcpassword"))
    bettor4 = Bettor(name = 'Sheyla', money = 3000,
                     broker = BROKER, auth = ("Sheyla", "Sheylapassword"))
    bettor5 = Bettor(name = 'Aly', money = 1500,
                     broker = BROKER, auth = ("Aly", "Alypassword"))
    bettor6 = Bettor(name = 'Jenny', money = 2000,
                     broker = BROKER, auth = ("Jenny", "Jennypassword"))
    bettor7 = Bettor(name = 'John', money = 1000,
                     broker = BROKER, auth = ("John", "Johnpassword"))
    bettor8 = Bettor(name = 'Justin', money = 3000,
                     broker = BROKER, auth = ("Justin", "Justinpassword"))
    bettor1.start()
    bettor2.start()
    bettor3.start()
    bettor4.start()
    bettor5.start()
    bettor6.start()
    bettor7.start()
    bettor8.start()


        
    



        
    
