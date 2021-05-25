
"""
Client.py
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

import select, sys, queue
from socket import *

class Client:
    def __init__(self):
       
        # do we keep a reference to some "entire block chain object"
        # or just two pointers as follows?
        self.lastConfirmedBlock = None
        self.lastReceivedBlock = None
        # and then we updated lastConfirmedBlock once a block has become x blocks away from lastReceivedBlock?  

        # dictionary to hold peers, their public keys and port numbers 
        self.peers = {}
        self.inputs = [sys.stdin]
        self.outputs = []
        self.address = 'localhost'
        self.myPort = 60002

        # Create a 

        

    
    # create a TCP connection with the tracker. 
    def connectToTracker(self):
        pass


    # given a peer from the tracker, open a TCP connection with this peer. 
    def connectToPeer(self):
        pass

    def joinChain(self):
        """Creates a TCP connection with a given tracker 
            by sending local ip and portnumber and public key 
        Receives a list of neighbors from the Tracker
        Opens a TCP with each of them and keeps track of that connection and their 
        respective public keys"""


    def runClient(self):
        while True:
            select.select(self.inputs, self.outputs, self.inputs)
        # run the actually client logic





    # uses Block Api to first mine, and then attempt to send a block to be included in the block chain
    def sendBlock(self):
        # if i receive a block during my attempt to mine and send a block what happens? 
        # do i give up on sending that block and just try to send another block? I mean i have to stop mining right? cause now what im hashing on
        # specifically "last hash" has changed. So do i just keep trying to get my message out over and over again until finally I get lucky enough and mine before anyone else. 
        # What if the proper Nonce value for the block I want to send is just super large? Then isnt linearly mining improper as it will always take longer to mine than a shorter Nonce ? but randoming mining would maybe check values multiple times and take much longer

        pass

    def receiveBlock(self):
        # this gets really tricky i think? Do we immediately assume its correct and then discard if we later see a longer fork?
        # how does a fork actually work? multiple blocks point the the same block as a 'previous' 
        # When do we discard 
        pass 

    def displayBlockChain(self):
        # I'm not sure how actual implementations of block chain / bitcoin tally the entire ledger / blockchain. Im pretty sure they use clever data stuctures / or just someone keeps track of their balance from the get-go 
        # but we need some way of displaying the entire block chain data... Maybe we only need to iterate over blocks we haven't iterated over and always keep track of the last block number that we have already tallied. 

        pass 


    # Generate private and public key pair so that we can sign our transactions and verify them... However maybe not necessary for the scope of the assignment
    def generateKeys(self):
        # most likely would just use an existing API for this 
       #  https://pycryptodome.readthedocs.io/en/latest/src/public_key/rsa.html
        pass
    
