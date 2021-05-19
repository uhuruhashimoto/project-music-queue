"""
Tracker.py
Group 7: Project Music Queue
CS60 Dartmouth Xia Zhou 

Jonah Weinbaum
James Fleming
Uhuru Hashimoto
Thomas White
Wendell Wu


This class allows a user to create a new client. 
Connect to the tracker and then all the peers, and then send and receive blocks use the block and blockchain API's

"""

import socket

# Port number that we open and wait for connections from clients
class Tracker:
    def __init__(self):
        self.listeningPort = 60005

        # A dictionary of all clients relating them by connection name to their ( public key , listening port number)
        # Will be parsed and sent to a new clients when a new client joins
        self.clients = {}
    
    # accepts a newClient. Tells all other clients to open a connection to this new client
    # adds the newClient to the client list
    def acceptNewClient():
        # most likely call "broadCastNewClient"
        pass


    # once a client signifies they are leaving we must tell everybody else 
    # remove client from 'clients'
    def removeClient():
        pass

    #tell all other clients they need to make a TCP connection with the new client 
    def broadCastNewClient():
        pass 











