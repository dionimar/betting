# Automatic betting manager

## About the code
This project is part of the Parallel Programming course at the Complutense University of Madrid.
It is a proof of concept for an automatic betting manager based on the mqtt protocol implemented in Python.

The project contains four files:
- Manager.py: in charge of managing the winners of the bets and publishing the results in the corresponding topics;
- Bettor.py: acts as a customer betting on a number of available objects;
- Seller.py: is the seller; publishes a list of available objects
- Observer.py: print the results of the winners of the bets in real time.

The files auth, mosquitto.conf, acl and password are used for setting up mosquitto with authentication (no TLS). 


## Authors
  - Daniel Lerchundi
  - Dioni Martinez
