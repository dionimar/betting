# betting
Automatic betting manager

This project is part of the Parallel Programming course at the Complutense University of Madrid.
It is a proof of concept for an automatic betting manager based on the mqtt protocol implemented in Python.

It consists of four files:
- Manager.py: in charge of managing the winners of the bets and publishing the results in the corresponding topics;
- Bettor.py: acts as a customer betting on a number of available objects;
- Seller.py: is the seller; publishes a list of available objects
- Observer.py: print the results of the winners of the bets in real time.



Written by:
  - Dani Lerchundi
  - Dioni Martinez
